"""用 Jinja2 渲染 AgentScope 项目模板。

# 参考 wiki: 技能系统详解/Scaffold 技能.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape


def _get_template_env() -> Environment:
    """获取 Jinja2 模板环境。"""
    return Environment(
        loader=PackageLoader("agent_cli_alicloud", "templates/agentscope"),
        autoescape=select_autoescape([]),
        keep_trailing_newline=True,
    )


def render_template(
    output_dir: Path,
    project_name: str,
    cli_version: str,
    template_name: str = "agentscope",
) -> list[Path]:
    """渲染项目模板到目标目录。

    Args:
        output_dir: 输出目录
        project_name: 项目名称
        cli_version: CLI 版本号
        template_name: 模板名称（当前仅支持 agentscope）

    Returns:
        生成的文件路径列表

    Raises:
        ValueError: 模板不存在或输出目录已存在且非空时抛出
    """
    if template_name != "agentscope":
        raise ValueError(
            f"不支持的模板: {template_name}，建议：当前仅支持 agentscope 模板"
        )

    env = _get_template_env()
    context = {
        "project_name": project_name,
        "cli_version": cli_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    # 模板文件到输出路径的映射
    template_files: list[tuple[str, str]] = [
        ("pyproject.toml.j2", "pyproject.toml"),
        ("README.md.j2", "README.md"),
        ("env.example.j2", ".env.example"),
        ("manifest.yaml.j2", "agent-cli-manifest.yaml"),
        ("src/agent/__init__.py.j2", "src/agent/__init__.py"),
        ("src/agent/main.py.j2", "src/agent/main.py"),
        ("src/agent/tools/__init__.py.j2", "src/agent/tools/__init__.py"),
        ("src/agent/tools/placeholder.py.j2", "src/agent/tools/placeholder.py"),
        ("tests/test_main.py.j2", "tests/test_main.py"),
    ]

    created_files: list[Path] = []

    for template_path, output_path in template_files:
        template = env.get_template(template_path)
        rendered = template.render(**context)

        file_path = output_dir / output_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(rendered, encoding="utf-8")
        created_files.append(file_path)

    return created_files
