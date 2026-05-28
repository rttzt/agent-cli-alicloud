"""agent-cli info 命令测试。"""

import json
from unittest.mock import patch

from typer.testing import CliRunner

from agent_cli_alicloud.cli import app
from agent_cli_alicloud.core.manifest import write_manifest

runner = CliRunner()


class TestInfoCommand:
    """info 命令测试集。"""

    def test_info_text_format(self, tmp_path):
        """text 格式应显示项目关键信息。"""
        # 先生成一个项目
        write_manifest(
            path=tmp_path,
            name="test-project",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        with patch("agent_cli_alicloud.cli.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["info"])

        assert result.exit_code == 0
        assert "test-project" in result.output
        assert "agentscope" in result.output
        assert "0.2.0" in result.output

    def test_info_json_format(self, tmp_path):
        """json 格式应输出合法 JSON。"""
        write_manifest(
            path=tmp_path,
            name="test-project",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        with patch("agent_cli_alicloud.cli.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["info", "--format", "json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == "test-project"
        assert data["template"]["name"] == "agentscope"
        assert data["cli_version"] == "0.2.0"

    def test_info_no_manifest(self, tmp_path):
        """无 manifest 时应返回错误。"""
        with patch("agent_cli_alicloud.cli.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["info"])

        assert result.exit_code == 1
        assert "未找到" in result.output

    def test_info_shows_all_fields(self, tmp_path):
        """text 格式应包含所有关键字段。"""
        write_manifest(
            path=tmp_path,
            name="full-info-test",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        with patch("agent_cli_alicloud.cli.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["info"])

        assert result.exit_code == 0
        assert "项目名称" in result.output
        assert "模板" in result.output
        assert "Agent 目录" in result.output
        assert "CLI 版本" in result.output
        assert "创建时间" in result.output
