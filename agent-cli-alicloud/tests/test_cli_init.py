"""agent-cli init 命令测试。"""


from typer.testing import CliRunner

from agent_cli_alicloud.cli import app

runner = CliRunner()


class TestInitCommand:
    """init 命令测试集。"""

    def test_init_success(self, tmp_path):
        """正常创建项目骨架。"""
        result = runner.invoke(app, ["init", "my-agent", "--dir", str(tmp_path)])
        assert result.exit_code == 0
        assert "已创建 my-agent/" in result.output
        assert (tmp_path / "my-agent" / "pyproject.toml").exists()
        assert (tmp_path / "my-agent" / "agent-cli-manifest.yaml").exists()
        assert (tmp_path / "my-agent" / "src" / "agent" / "main.py").exists()

    def test_init_with_template_option(self, tmp_path):
        """指定 --template agentscope 应成功。"""
        result = runner.invoke(
            app, ["init", "my-agent", "--template", "agentscope", "--dir", str(tmp_path)]
        )
        assert result.exit_code == 0
        assert "模板: agentscope" in result.output

    def test_init_invalid_name_uppercase(self, tmp_path):
        """大写字母名称应被拒绝。"""
        result = runner.invoke(app, ["init", "MyAgent", "--dir", str(tmp_path)])
        assert result.exit_code == 1
        assert "不合法" in result.output

    def test_init_invalid_name_starts_with_number(self, tmp_path):
        """数字开头的名称应被拒绝。"""
        result = runner.invoke(app, ["init", "123-agent", "--dir", str(tmp_path)])
        assert result.exit_code == 1
        assert "不合法" in result.output

    def test_init_invalid_name_special_chars(self, tmp_path):
        """包含特殊字符的名称应被拒绝。"""
        result = runner.invoke(app, ["init", "my_agent!", "--dir", str(tmp_path)])
        assert result.exit_code == 1
        assert "不合法" in result.output

    def test_init_invalid_name_too_short(self, tmp_path):
        """单字符名称应被拒绝（正则要求至少 2 字符）。"""
        result = runner.invoke(app, ["init", "a", "--dir", str(tmp_path)])
        assert result.exit_code == 1
        assert "不合法" in result.output

    def test_init_existing_dir_no_force(self, tmp_path):
        """已存在非空目录且不带 --force 应失败。"""
        project_dir = tmp_path / "my-agent"
        project_dir.mkdir()
        (project_dir / "existing.txt").write_text("占位")

        result = runner.invoke(app, ["init", "my-agent", "--dir", str(tmp_path)])
        assert result.exit_code == 1
        assert "已存在" in result.output

    def test_init_existing_dir_with_force(self, tmp_path):
        """已存在目录带 --force 应覆盖成功。"""
        project_dir = tmp_path / "my-agent"
        project_dir.mkdir()
        (project_dir / "existing.txt").write_text("占位")

        result = runner.invoke(app, ["init", "my-agent", "--dir", str(tmp_path), "--force"])
        assert result.exit_code == 0
        assert "已创建 my-agent/" in result.output

    def test_init_invalid_template(self, tmp_path):
        """不支持的模板应返回错误。"""
        result = runner.invoke(
            app, ["init", "my-agent", "--template", "nonexistent", "--dir", str(tmp_path)]
        )
        assert result.exit_code == 1
        assert "不支持的模板" in result.output

    def test_init_generates_all_files(self, tmp_path):
        """init 应生成完整的文件列表。"""
        result = runner.invoke(app, ["init", "test-project", "--dir", str(tmp_path)])
        assert result.exit_code == 0

        project_dir = tmp_path / "test-project"
        expected_files = [
            "pyproject.toml",
            "README.md",
            ".env.example",
            "agent-cli-manifest.yaml",
            "src/agent/__init__.py",
            "src/agent/main.py",
            "src/agent/tools/__init__.py",
            "src/agent/tools/placeholder.py",
            "tests/test_main.py",
        ]
        for f in expected_files:
            assert (project_dir / f).exists(), f"缺少文件: {f}"
