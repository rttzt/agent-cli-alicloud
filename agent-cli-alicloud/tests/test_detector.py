"""检测器测试 — mock 目录存在与不存在场景。"""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_cli_alicloud.core.detector import (
    DetectedAgent,
    detect_agents,
)


class TestDetectAgents:
    """detect_agents 测试集。"""

    def test_returns_all_four_agents(self):
        """无 target 时应返回 4 个 Agent 结果。"""
        agents = detect_agents()
        assert len(agents) == 4

    def test_agent_names(self):
        """应包含所有预定义 Agent 名称。"""
        agents = detect_agents()
        names = {a.name for a in agents}
        assert names == {"Qoder", "通义灵码", "Claude Code", "Cursor"}

    @patch("agent_cli_alicloud.core.detector._is_agent_installed", return_value=True)
    def test_all_detected_when_dirs_exist(self, mock_installed):
        """所有 Agent 已安装时 detected 应全为 True。"""
        agents = detect_agents()
        assert all(a.detected for a in agents)

    @patch("agent_cli_alicloud.core.detector._is_agent_installed", return_value=False)
    def test_none_detected_when_dirs_missing(self, mock_installed):
        """所有 Agent 未安装时 detected 应全为 False。"""
        agents = detect_agents()
        assert not any(a.detected for a in agents)

    def test_target_filter_qoder(self):
        """指定 target=qoder 应只返回 Qoder。"""
        agents = detect_agents(target="qoder")
        assert len(agents) == 1
        assert agents[0].name == "Qoder"

    def test_target_filter_cursor(self):
        """指定 target=cursor 应只返回 Cursor。"""
        agents = detect_agents(target="cursor")
        assert len(agents) == 1
        assert agents[0].name == "Cursor"
        assert agents[0].install_pattern == "file"

    def test_target_filter_lingma(self):
        """指定 target=lingma 应只返回通义灵码。"""
        agents = detect_agents(target="lingma")
        assert len(agents) == 1
        assert agents[0].name == "通义灵码"

    def test_target_filter_claude_code(self):
        """指定 target=claude-code 应只返回 Claude Code。"""
        agents = detect_agents(target="claude-code")
        assert len(agents) == 1
        assert agents[0].name == "Claude Code"

    def test_invalid_target_raises(self):
        """无效 target 应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不支持的目标"):
            detect_agents(target="vscode")


class TestDetectedAgent:
    """DetectedAgent 数据类测试。"""

    def test_get_install_path_dir_pattern(self):
        """dir 模式安装路径应为 skills_dir/name/SKILL.md。"""
        agent = DetectedAgent(
            name="Qoder",
            skills_dir=Path("/home/user/.qoder/skills"),
            detected=True,
            install_pattern="dir",
        )
        path = agent.get_install_path("agent-cli-alicloud-workflow")
        assert path == Path("/home/user/.qoder/skills/agent-cli-alicloud-workflow/SKILL.md")

    def test_get_install_path_file_pattern(self):
        """file 模式安装路径应为 skills_dir/name.md。"""
        agent = DetectedAgent(
            name="Cursor",
            skills_dir=Path("/home/user/.cursor/rules"),
            detected=True,
            install_pattern="file",
        )
        path = agent.get_install_path("agent-cli-alicloud-workflow")
        assert path == Path("/home/user/.cursor/rules/agent-cli-alicloud-workflow.md")

    def test_detected_flag(self):
        """detected 属性应如实反映。"""
        agent_true = DetectedAgent(
            name="Test", skills_dir=Path("/tmp"), detected=True, install_pattern="dir"
        )
        agent_false = DetectedAgent(
            name="Test", skills_dir=Path("/tmp"), detected=False, install_pattern="dir"
        )
        assert agent_true.detected is True
        assert agent_false.detected is False


class TestIsAgentInstalled:
    """_is_agent_installed 综合检测逻辑测试。"""

    def test_skills_dir_exists_returns_true(self, tmp_path):
        """skills 目录存在时应返回 True（即使无 executable）。"""
        from agent_cli_alicloud.core.detector import _is_agent_installed

        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        assert _is_agent_installed(skills_dir, "", "") is True

    def test_nothing_exists_returns_false(self, tmp_path):
        """什么都不存在时应返回 False。"""
        from agent_cli_alicloud.core.detector import _is_agent_installed

        skills_dir = tmp_path / "nonexistent" / "skills"
        assert _is_agent_installed(skills_dir, "", "") is False

    @patch("agent_cli_alicloud.core.detector.shutil.which", return_value="/usr/local/bin/qoder")
    def test_executable_found_returns_true(self, mock_which, tmp_path):
        """可执行文件在 PATH 中时应返回 True（即使 skills 目录不存在）。"""
        from agent_cli_alicloud.core.detector import _is_agent_installed

        skills_dir = tmp_path / "nonexistent" / "skills"
        assert _is_agent_installed(skills_dir, "qoder", "") is True

    def test_config_file_found_returns_true(self, tmp_path):
        """配置目录存在时应返回 True。"""
        from agent_cli_alicloud.core.detector import _is_agent_installed

        skills_dir = tmp_path / "nonexistent" / "skills"
        config_dir = tmp_path / ".test-agent"
        config_dir.mkdir()
        # 用 monkeypatch 模拟 home 目录比较复杂，直接测试 config 路径存在的情况
        # 这里通过 patch Path.home 实现
        with patch("agent_cli_alicloud.core.detector.Path.home", return_value=tmp_path):
            assert _is_agent_installed(skills_dir, "", ".test-agent") is True
