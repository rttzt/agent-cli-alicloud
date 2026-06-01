"""agent-cli-alicloud CLI 入口。

# 参考 wiki: CLI 命令参考/项目管理命令.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated, Literal, Optional

import typer

from agent_cli_alicloud import TEMPLATE_VERSION, __version__
from agent_cli_alicloud.core.detector import detect_agents
from agent_cli_alicloud.core.installer import SKILL_NAMES, install_skills
from agent_cli_alicloud.core.manifest import read_manifest, write_manifest
from agent_cli_alicloud.core.scaffold import render_template

app = typer.Typer(
    name="agent-cli",
    help="阿里云 Agent 开发脚手架 CLI — 确定性执行层",
    no_args_is_help=True,
)

# 项目名称校验正则
_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,63}$")


@app.command()
def setup(
    target: Annotated[
        Optional[str],
        typer.Option(
            "--target",
            "-t",
            help="指定目标 Coding Agent（qoder|lingma|claude-code|cursor），默认全部检测",
        ),
    ] = None,
) -> None:
    """检测本机 Coding Agent 并安装 Skills。"""
    # 参考 wiki: CLI 命令参考/项目管理命令.md
    try:
        agents = detect_agents(target)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    detected_agents = [a for a in agents if a.detected]
    skipped_agents = [a for a in agents if not a.detected]

    # 显示检测结果
    for agent in detected_agents:
        typer.echo(f"✓ 检测到: {agent.name} ({agent.skills_dir})")
    for agent in skipped_agents:
        typer.echo(f"✗ 跳过: {agent.name} (未安装)")

    if not detected_agents:
        typer.echo(
            "\n未检测到任何已安装的 Coding Agent，建议：安装 Qoder / 通义灵码 / Claude Code / Cursor 后重试",
            err=True,
        )
        raise typer.Exit(code=1)

    # 安装 Skills
    try:
        results = install_skills(detected_agents)
    except (OSError, FileNotFoundError) as e:
        typer.echo(
            f"安装 Skills 失败: {e}，建议：检查目标目录写入权限后重试",
            err=True,
        )
        raise typer.Exit(code=1)

    # 统计
    total_agents = len(results)
    typer.echo(f"\n已安装 {len(SKILL_NAMES)} 个 skills 到 {total_agents} 个 coding agents:")
    for skill_name in SKILL_NAMES:
        typer.echo(f"  - {skill_name}")

    typer.echo(
        '\n下一步: 打开你的 coding agent，告诉它你的想法，例如：\n'
        '  "我想做一个小红书爆文分析 Agent，请用 agent-cli-alicloud"'
    )


@app.command()
def init(
    name: Annotated[
        str,
        typer.Argument(
            help="项目名称（小写字母开头，仅含小写字母、数字和连字符）",
        ),
    ],
    template: Annotated[
        str,
        typer.Option(
            "--template",
            "-t",
            help="项目模板",
        ),
    ] = "agentscope",
    dir: Annotated[
        Optional[str],
        typer.Option(
            "--dir",
            "-d",
            help="输出目录（默认当前目录）",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="覆盖已存在的目录",
        ),
    ] = False,
) -> None:
    """生成 Agent 项目骨架（纯模板渲染，不调用 LLM）。"""
    # 参考 wiki: CLI 命令参考/项目管理命令.md

    # 校验 name
    if not _NAME_PATTERN.match(name):
        typer.echo(
            f"项目名称 '{name}' 不合法，建议：使用小写字母开头，仅含小写字母、数字和连字符，长度 2-64",
            err=True,
        )
        raise typer.Exit(code=1)

    # 确定输出目录
    base_dir = Path(dir) if dir else Path.cwd()
    output_dir = base_dir / name

    # 检查目录是否已存在
    if output_dir.exists() and not force:
        if any(output_dir.iterdir()):
            typer.echo(
                f"目录 {output_dir} 已存在且非空，建议：使用 --force 覆盖或选择其他目录",
                err=True,
            )
            raise typer.Exit(code=1)

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 渲染模板
    try:
        created_files = render_template(
            output_dir=output_dir,
            project_name=name,
            cli_version=__version__,
            template_name=template,
        )
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    # 写入 manifest
    write_manifest(
        path=output_dir,
        name=name,
        template_name=template,
        template_version=TEMPLATE_VERSION,
        agent_directory="src/agent",
        cli_version=__version__,
    )

    # 显示结果
    typer.echo(f"✓ 已创建 {name}/ (模板: {template})")

    # 显示文件树
    for file_path in sorted(created_files):
        rel_path = file_path.relative_to(output_dir)
        typer.echo(f"  ├── {rel_path}")
    typer.echo("  └── agent-cli-manifest.yaml")

    typer.echo("\n下一步: 在你的 coding agent 中打开此目录，让它填充设计文档。")


@app.command()
def info(
    format: Annotated[
        Literal["text", "json"],
        typer.Option(
            "--format",
            "-f",
            help="输出格式（text|json）",
            case_sensitive=False,
        ),
    ] = "text",
) -> None:
    """读取 manifest 并展示项目状态。"""
    # 参考 wiki: CLI 命令参考/项目管理命令.md
    cwd = Path.cwd()

    try:
        manifest = read_manifest(cwd)
    except FileNotFoundError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    if format == "json":
        typer.echo(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        typer.echo(f"项目名称: {manifest.get('name', '未知')}")
        template = manifest.get("template", {})
        typer.echo(f"模板: {template.get('name', '未知')} v{template.get('version', '?')}")
        typer.echo(f"Agent 目录: {manifest.get('agent_directory', '未知')}")
        typer.echo(f"CLI 版本: {manifest.get('cli_version', '未知')}")
        typer.echo(f"创建时间: {manifest.get('created_at', '未知')}")


@app.command()
def version() -> None:
    """显示 CLI 版本号。"""
    typer.echo(f"agent-cli-alicloud v{__version__}")


if __name__ == "__main__":
    app()
