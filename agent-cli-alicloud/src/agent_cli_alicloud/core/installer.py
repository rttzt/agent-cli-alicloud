"""从包内 skills/ 目录安装 SKILL.md 到 Coding Agent。

# 参考 wiki: 技能系统详解/技能系统详解.md
"""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

from agent_cli_alicloud.core.detector import DetectedAgent

# 内置 Skills 列表
SKILL_NAMES: list[str] = [
    "agent-cli-alicloud-workflow",
    "agent-cli-alicloud-scaffold",
    "agent-cli-alicloud-deploy",
    "agent-cli-alicloud-eval",
]


def _get_skill_source_path(skill_name: str) -> Path:
    """获取包内 Skill 源文件路径。

    Args:
        skill_name: Skill 名称

    Returns:
        Skill 源文件路径

    Raises:
        FileNotFoundError: Skill 文件不存在时抛出
    """
    # 使用 importlib.resources 定位包内资源
    package_ref = resources.files("agent_cli_alicloud") / "skills" / skill_name / "SKILL.md"
    # 获取真实路径
    source_path = Path(str(package_ref))
    if not source_path.exists():
        raise FileNotFoundError(
            f"内置 Skill 文件不存在: {skill_name}，建议：重新安装 agent-cli-alicloud"
        )
    return source_path


def install_skills(agents: list[DetectedAgent]) -> dict[str, list[str]]:
    """将所有内置 Skills 安装到检测到的 Coding Agent。

    Args:
        agents: 已检测到（detected=True）的 Agent 列表

    Returns:
        安装结果字典，key 为 Agent 名称，value 为已安装的 Skill 名称列表

    Raises:
        FileNotFoundError: Skill 源文件不存在时抛出
    """
    results: dict[str, list[str]] = {}

    for agent in agents:
        if not agent.detected:
            continue

        installed: list[str] = []

        for skill_name in SKILL_NAMES:
            source_path = _get_skill_source_path(skill_name)
            target_path = agent.get_install_path(skill_name)

            # 确保目标目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if agent.install_pattern == "file":
                # Cursor: 直接复制 SKILL.md 内容为 .md 文件
                shutil.copy2(source_path, target_path)
            else:
                # 标准模式: 复制到 {skills_dir}/{name}/SKILL.md
                shutil.copy2(source_path, target_path)

            installed.append(skill_name)

        results[agent.name] = installed

    return results
