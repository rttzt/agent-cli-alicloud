"""agent-cli setup 命令测试。"""

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from agent_cli_alicloud.cli import app
from agent_cli_alicloud.core.detector import DetectedAgent

runner = CliRunner()


def _make_agent(name: str, detected: bool, pattern: str = "dir") -> DetectedAgent:
    """构建测试用 DetectedAgent。"""
    return DetectedAgent(
        name=name,
        skills_dir=Path(f"/tmp/test-{name.lower()}/skills"),
        detected=detected,
        install_pattern=pattern,
    )


class TestSetupCommand:
    """setup 命令测试集。"""

    @patch("agent_cli_alicloud.cli.install_skills")
    @patch("agent_cli_alicloud.cli.detect_agents")
    def test_setup_success(self, mock_detect, mock_install):
        """检测到 Agent 时应成功安装 Skills。"""
        mock_detect.return_value = [
            _make_agent("Qoder", detected=True),
        ]
        mock_install.return_value = {"Qoder": ["agent-cli-alicloud-workflow"]}

        result = runner.invoke(app, ["setup"])
        assert result.exit_code == 0
        assert "检测到" in result.output
        assert "Qoder" in result.output

    @patch("agent_cli_alicloud.cli.detect_agents")
    def test_setup_no_agents(self, mock_detect):
        """无 Agent 检测到时应返回错误。"""
        mock_detect.return_value = [
            _make_agent("Qoder", detected=False),
            _make_agent("Cursor", detected=False, pattern="file"),
        ]

        result = runner.invoke(app, ["setup"])
        assert result.exit_code == 1
        assert "未检测到" in result.output

    @patch("agent_cli_alicloud.cli.detect_agents")
    def test_setup_invalid_target(self, mock_detect):
        """无效 target 应返回错误。"""
        mock_detect.side_effect = ValueError("不支持的目标 Agent: foo，建议：使用 qoder, lingma 之一")

        result = runner.invoke(app, ["setup", "--target", "foo"])
        assert result.exit_code == 1
        assert "不支持的目标" in result.output

    @patch("agent_cli_alicloud.cli.install_skills")
    @patch("agent_cli_alicloud.cli.detect_agents")
    def test_setup_partial_detection(self, mock_detect, mock_install):
        """部分 Agent 检测到时应显示跳过信息。"""
        mock_detect.return_value = [
            _make_agent("Qoder", detected=True),
            _make_agent("Cursor", detected=False, pattern="file"),
        ]
        mock_install.return_value = {"Qoder": ["agent-cli-alicloud-workflow"]}

        result = runner.invoke(app, ["setup"])
        assert result.exit_code == 0
        assert "跳过" in result.output
        assert "Cursor" in result.output
