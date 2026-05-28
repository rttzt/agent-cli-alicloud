"""Golden snapshot 测试 — 验证 agent-cli init 的确定性输出。

核心原则：不依赖 LLM、不依赖网络、不依赖 DashScope API key。
任何 contributor 在离线环境下都能跑通。
"""

from pathlib import Path

import yaml
from typer.testing import CliRunner

from agent_cli_alicloud.cli import app

runner = CliRunner()
GOLDEN_DIR = Path(__file__).parent / "xiaohongshu_demo"


def test_directory_tree(tmp_path):
    """验证 init 生成的目录树与 golden snapshot 一致。"""
    result = runner.invoke(app, ["init", "xiaohongshu-trend-agent", "--dir", str(tmp_path)])
    assert result.exit_code == 0

    # 生成实际目录树
    project_dir = tmp_path / "xiaohongshu-trend-agent"
    actual_files = sorted(
        str(p.relative_to(project_dir))
        for p in project_dir.rglob("*") if p.is_file()
    )

    expected = (GOLDEN_DIR / "expected_tree.txt").read_text().strip().splitlines()
    assert actual_files == sorted(expected)


def test_manifest_content(tmp_path):
    """验证 manifest YAML 内容（除 created_at）与 golden snapshot 一致。"""
    result = runner.invoke(app, ["init", "xiaohongshu-trend-agent", "--dir", str(tmp_path)])
    assert result.exit_code == 0

    actual_manifest = yaml.safe_load(
        (tmp_path / "xiaohongshu-trend-agent" / "agent-cli-manifest.yaml").read_text()
    )
    expected_manifest = yaml.safe_load(
        (GOLDEN_DIR / "expected_manifest.yaml").read_text()
    )

    # 移除时间戳字段比较
    actual_manifest.pop("created_at", None)
    expected_manifest.pop("created_at", None)
    assert actual_manifest == expected_manifest


def test_pyproject_snapshot(tmp_path):
    """验证生成的 pyproject.toml 与 golden snapshot 一致。"""
    result = runner.invoke(app, ["init", "xiaohongshu-trend-agent", "--dir", str(tmp_path)])
    assert result.exit_code == 0

    actual = (tmp_path / "xiaohongshu-trend-agent" / "pyproject.toml").read_text()
    expected = (GOLDEN_DIR / "expected_pyproject.toml").read_text()
    assert actual == expected


def test_main_py_snapshot(tmp_path):
    """验证 src/agent/main.py 与 golden snapshot 一致。"""
    result = runner.invoke(app, ["init", "xiaohongshu-trend-agent", "--dir", str(tmp_path)])
    assert result.exit_code == 0

    actual = (tmp_path / "xiaohongshu-trend-agent" / "src" / "agent" / "main.py").read_text()
    expected = (GOLDEN_DIR / "expected_main.py").read_text()
    assert actual == expected
