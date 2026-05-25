"""init 命令的 4 步业务编排：澄清 → 文档生成 → 脚手架 → 完成提示"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from agent_cli_alicloud.core import llm

# ---------------------------------------------------------------------------
# Jinja2 环境
# ---------------------------------------------------------------------------

_TEMPLATE_DIR: Path = Path(__file__).parent.parent / "templates"

_env: Environment = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    undefined=StrictUndefined,
    keep_trailing_newline=True,
)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def _parse_json_response(text: str) -> dict[str, Any]:
    """解析 LLM 返回的 JSON，处理可能的 markdown 代码块包裹。"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:])
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM 返回的 JSON 解析失败：{exc}，"
            f"建议：检查 LLM 响应是否符合 Prompt 中要求的 JSON 格式"
        ) from exc
    if not isinstance(result, dict):
        raise ValueError(
            "LLM 返回的 JSON 顶层结构不是 object，"
            "建议：检查 Prompt 是否要求返回 dict 形式的 JSON"
        )
    return result


def _render(template_name: str, **context: Any) -> str:
    """渲染指定 Jinja2 模板。"""
    template = _env.get_template(template_name)
    return template.render(**context)


def _write_file(path: Path, content: str) -> None:
    """写入文件，自动创建父目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _format_clarification_text(questions: list[dict[str, str]]) -> str:
    """将澄清问答格式化为字符串，供下一步 Prompt 使用。"""
    parts: list[str] = []
    for idx, q in enumerate(questions, start=1):
        parts.append(
            f"{idx}. [{q['category']}] {q['question']}\n   答：{q['answer']}"
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def run_init(idea: str, output_dir: str, yes: bool = False) -> None:
    """执行 init 命令的 4 步流程。

    Args:
        idea: 用户的 Agent 想法（一句话）
        output_dir: 输出目录
        yes: True 时跳过交互确认，直接使用默认答案
    """
    if not idea or not idea.strip():
        raise ValueError("idea 不能为空，建议：用一句话描述你的 Agent 想法")

    typer.echo("🚀 agent-cli init — 从想法到设计文档")
    typer.echo("")

    # ----- [1/4] 澄清问题 -----
    questions = _step_clarification(idea, yes=yes)

    # ----- [2/4] 文档生成 -----
    doc_data, project_dir, generated_docs = _step_documents(
        idea=idea,
        questions=questions,
        output_dir=output_dir,
    )

    # ----- [3/4] 脚手架 -----
    generated_scaffold = _step_scaffold(project_dir=project_dir, doc_data=doc_data)

    # ----- [4/4] 完成提示 -----
    _step_finish(
        project_dir=project_dir,
        doc_data=doc_data,
        generated_docs=generated_docs,
        generated_scaffold=generated_scaffold,
    )


# ---------------------------------------------------------------------------
# 各步骤实现
# ---------------------------------------------------------------------------


def _step_clarification(idea: str, yes: bool) -> list[dict[str, str]]:
    """[1/4] 调用 LLM 生成澄清问题，并展示给用户确认。"""
    typer.echo("[1/4] 生成澄清问题...")
    typer.echo("")

    prompt = llm.CLARIFICATION_PROMPT.replace("{idea}", idea)
    raw = llm.call_llm(prompt, system=llm.SYSTEM_PROMPT)
    parsed = _parse_json_response(raw)

    raw_questions = parsed.get("questions")
    if not isinstance(raw_questions, list) or not raw_questions:
        raise ValueError(
            "LLM 未返回有效的澄清问题列表，"
            "建议：检查 CLARIFICATION_PROMPT 是否引导 LLM 输出 questions 数组"
        )

    questions: list[dict[str, str]] = []
    for item in raw_questions:
        if not isinstance(item, dict):
            raise ValueError(
                "澄清问题项格式不正确，建议：每个问题需包含 category/question/default_answer 字段"
            )
        category = str(item.get("category", "")).strip()
        question = str(item.get("question", "")).strip()
        default_answer = str(item.get("default_answer", "")).strip()
        if not (category and question and default_answer):
            raise ValueError(
                "澄清问题缺少必要字段，建议：检查 LLM 返回的 category/question/default_answer 是否完整"
            )
        questions.append(
            {
                "category": category,
                "question": question,
                "answer": default_answer,
            }
        )

    for idx, q in enumerate(questions, start=1):
        typer.echo(f"  {idx}. {q['category']}：{q['question']}")
        typer.echo(f"     默认答案：{q['answer']}")
        typer.echo("")

    if not yes:
        accepted = typer.confirm("是否接受以上默认答案？", default=True)
        if not accepted:
            typer.echo("（MVP 阶段暂不支持自定义输入，将继续使用默认答案）")
        typer.echo("")

    return questions


def _step_documents(
    idea: str,
    questions: list[dict[str, str]],
    output_dir: str,
) -> tuple[dict[str, Any], Path, list[str]]:
    """[2/4] 调用 LLM 生成文档数据并渲染 4 份 markdown。"""
    typer.echo("[2/4] 生成设计文档...")

    clarification_text = _format_clarification_text(questions)
    prompt = (
        llm.DOCUMENT_GEN_PROMPT
        .replace("{idea}", idea)
        .replace("{clarification}", clarification_text)
    )
    raw = llm.call_llm(prompt, system=llm.SYSTEM_PROMPT)
    doc_data = _parse_json_response(raw)

    project_name = str(doc_data.get("project_name", "")).strip()
    if not project_name:
        raise ValueError(
            "文档数据缺少 project_name 字段，"
            "建议：检查 DOCUMENT_GEN_PROMPT 是否引导 LLM 输出 project_name"
        )

    project_dir = Path(output_dir).resolve() / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    # 渲染并写入 4 份文档
    docs: list[tuple[str, str, dict[str, Any]]] = [
        (
            "agents_md.j2",
            "AGENTS.md",
            doc_data,
        ),
        (
            "scope_md.j2",
            "scope.md",
            doc_data,
        ),
        (
            "eval_plan_md.j2",
            "eval-plan.md",
            doc_data,
        ),
        (
            "clarification_md.j2",
            "clarification.md",
            {"idea": idea, "questions": questions},
        ),
    ]

    generated: list[str] = []
    for tpl, out_name, ctx in docs:
        content = _render(tpl, **ctx)
        _write_file(project_dir / out_name, content)
        typer.echo(f"  ✓ {out_name}")
        generated.append(out_name)

    typer.echo("")
    return doc_data, project_dir, generated


def _step_scaffold(project_dir: Path, doc_data: dict[str, Any]) -> list[str]:
    """[3/4] 渲染脚手架模板，生成项目骨架。"""
    typer.echo("[3/4] 生成项目脚手架...")

    items: list[tuple[str, str]] = [
        ("scaffold_pyproject.j2", "pyproject.toml"),
        ("scaffold_agent_init.j2", "src/agent/__init__.py"),
        ("scaffold_main.j2", "src/agent/main.py"),
        ("scaffold_tools_init.j2", "src/agent/tools/__init__.py"),
        ("scaffold_tool.j2", "src/agent/tools/xhs_search.py"),
        ("scaffold_test.j2", "tests/test_main.py"),
    ]

    generated: list[str] = []
    for tpl, rel_path in items:
        content = _render(tpl, **doc_data)
        _write_file(project_dir / rel_path, content)
        typer.echo(f"  ✓ {rel_path}")
        generated.append(rel_path)

    typer.echo("")
    return generated


def _step_finish(
    project_dir: Path,
    doc_data: dict[str, Any],
    generated_docs: list[str],
    generated_scaffold: list[str],
) -> None:
    """[4/4] 渲染 next-steps.md 并打印完成摘要。"""
    typer.echo("[4/4] 完成！")
    typer.echo("")

    next_steps_content = _render("next_steps_md.j2", **doc_data)
    _write_file(project_dir / "next-steps.md", next_steps_content)

    total_files = len(generated_docs) + len(generated_scaffold) + 1  # +1: next-steps.md

    try:
        rel_dir = project_dir.relative_to(Path.cwd())
        display_dir = f"./{rel_dir}/"
    except ValueError:
        display_dir = f"{project_dir}/"

    typer.echo(f"📁 项目已生成到：{display_dir}")
    typer.echo(f"📄 生成了 {total_files} 个文件")
    typer.echo("👉 下一步：查看 next-steps.md 了解后续任务")
