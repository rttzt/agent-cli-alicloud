"""agent-cli-alicloud 核心模块。"""

from agent_cli_alicloud.core.detector import DetectedAgent, detect_agents
from agent_cli_alicloud.core.installer import install_skills
from agent_cli_alicloud.core.manifest import read_manifest, write_manifest
from agent_cli_alicloud.core.scaffold import render_template

__all__ = [
    "read_manifest",
    "write_manifest",
    "detect_agents",
    "DetectedAgent",
    "render_template",
    "install_skills",
]
