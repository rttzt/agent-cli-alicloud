"""CLI 入口 — typer app 注册"""

from typing import Annotated

import typer

from agent_cli_alicloud.core.init_flow import run_init

app = typer.Typer(
    name="agent-cli",
    help="让任意 Coding Agent 把一句模糊的 Agent 想法，5 分钟内变成结构化设计文档 + 可运行脚手架",
)


@app.callback()
def callback() -> None:
    """agent-cli-alicloud：Agent 想法到设计文档的 CLI 工具"""


@app.command()
def init(
    idea: Annotated[str, typer.Argument(help="你的 Agent 想法，一句话描述")],
    output_dir: Annotated[
        str, typer.Option("--output-dir", "-o", help="输出目录")
    ] = ".",
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="跳过确认，直接使用默认答案")
    ] = False,
) -> None:
    """从一句话 idea 生成 Agent 设计文档和项目脚手架"""
    run_init(idea=idea, output_dir=output_dir, yes=yes)


if __name__ == "__main__":
    app()
