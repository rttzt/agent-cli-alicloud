"""Golden snapshot 测试 — 验证 init 命令的输出与预期一致"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Golden snapshot 目录
GOLDEN_DIR = Path(__file__).parent / "golden" / "xiaohongshu_demo"

# init 命令生成的项目名（来自 Mock 数据）
PROJECT_NAME = "xiaohongshu-trend-agent"

# Mock 模式下使用的 idea 文案（与生成 golden 时保持一致）
IDEA = "我想做一个能帮品牌方分析小红书爆文的 Agent"

# 预期文件列表
EXPECTED_FILES = [
    "AGENTS.md",
    "scope.md",
    "eval-plan.md",
    "clarification.md",
    "next-steps.md",
    "pyproject.toml",
    "src/agent/__init__.py",
    "src/agent/main.py",
    "src/agent/tools/__init__.py",
    "src/agent/tools/xhs_search.py",
    "tests/test_main.py",
]


def _ensure_mock_mode() -> None:
    """移除 DASHSCOPE_API_KEY，确保 LLM 走 Mock 分支。"""
    os.environ.pop("DASHSCOPE_API_KEY", None)


def test_golden_files_exist() -> None:
    """验证 golden snapshot 目录包含所有预期文件"""
    for file_path in EXPECTED_FILES:
        full_path = GOLDEN_DIR / file_path
        assert full_path.exists(), f"Golden snapshot 缺少文件：{file_path}"


def test_init_generates_expected_structure() -> None:
    """验证 init 命令在 Mock 模式下生成与 golden snapshot 一致的目录结构"""
    _ensure_mock_mode()

    with tempfile.TemporaryDirectory() as tmpdir:
        from agent_cli_alicloud.core.init_flow import run_init

        run_init(
            idea=IDEA,
            output_dir=tmpdir,
            yes=True,
        )

        project_dir = Path(tmpdir) / PROJECT_NAME

        for file_path in EXPECTED_FILES:
            full_path = project_dir / file_path
            assert full_path.exists(), f"init 命令未生成文件：{file_path}"


def test_init_output_matches_golden() -> None:
    """验证 init 命令的输出内容与 golden snapshot 一致"""
    _ensure_mock_mode()

    with tempfile.TemporaryDirectory() as tmpdir:
        from agent_cli_alicloud.core.init_flow import run_init

        run_init(
            idea=IDEA,
            output_dir=tmpdir,
            yes=True,
        )

        project_dir = Path(tmpdir) / PROJECT_NAME

        for file_path in EXPECTED_FILES:
            golden_file = GOLDEN_DIR / file_path
            generated_file = project_dir / file_path

            golden_content = golden_file.read_text(encoding="utf-8")
            generated_content = generated_file.read_text(encoding="utf-8")

            assert golden_content == generated_content, (
                f"文件 {file_path} 内容与 golden snapshot 不一致"
            )
