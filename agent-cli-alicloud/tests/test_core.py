"""agent-cli-alicloud 基础测试。"""

from pathlib import Path

from agent_cli_alicloud import __version__
from agent_cli_alicloud.core.detector import DetectedAgent, detect_agents
from agent_cli_alicloud.core.manifest import (
    read_manifest,
    write_manifest,
)


def test_version() -> None:
    """版本号应为 0.2.0。"""
    assert __version__ == "0.2.0"


def test_write_and_read_manifest(tmp_path: Path) -> None:
    """写入 manifest 后应能正确读回。"""
    write_manifest(
        path=tmp_path,
        name="test-project",
        template_name="agentscope",
        template_version="0.1.0",
        agent_directory="src/agent",
        cli_version="0.2.0",
    )

    manifest = read_manifest(tmp_path)
    assert manifest["name"] == "test-project"
    assert manifest["template"]["name"] == "agentscope"
    assert manifest["schema_version"] == 1
    assert manifest["cli_version"] == "0.2.0"


def test_read_manifest_not_found(tmp_path: Path) -> None:
    """不存在 manifest 时应抛出 FileNotFoundError。"""
    import pytest

    with pytest.raises(FileNotFoundError, match="未找到"):
        read_manifest(tmp_path)


def test_detect_agents_returns_list() -> None:
    """detect_agents 应返回列表。"""
    agents = detect_agents()
    assert isinstance(agents, list)
    assert len(agents) == 4  # 4 种 Coding Agent


def test_detect_agents_invalid_target() -> None:
    """无效 target 应抛出 ValueError。"""
    import pytest

    with pytest.raises(ValueError, match="不支持的目标"):
        detect_agents(target="invalid")


def test_detected_agent_install_path() -> None:
    """DetectedAgent.get_install_path 应返回正确路径。"""
    agent_dir = DetectedAgent(
        name="Qoder",
        skills_dir=Path("/tmp/skills"),
        detected=True,
        install_pattern="dir",
    )
    path = agent_dir.get_install_path("agent-cli-alicloud-workflow")
    assert path == Path("/tmp/skills/agent-cli-alicloud-workflow/SKILL.md")

    agent_file = DetectedAgent(
        name="Cursor",
        skills_dir=Path("/tmp/rules"),
        detected=True,
        install_pattern="file",
    )
    path = agent_file.get_install_path("agent-cli-alicloud-workflow")
    assert path == Path("/tmp/rules/agent-cli-alicloud-workflow.md")
