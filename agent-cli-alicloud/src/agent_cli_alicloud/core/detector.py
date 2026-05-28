"""检测本机已安装的 Coding Agent 并返回 skills 安装路径。

# 参考 wiki: 技能系统详解/技能系统详解.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# 各 Coding Agent 的 skills 目录检测路径和安装模式
# 参考 wiki: 核心概念/技能系统原理.md
_AGENT_CONFIGS: list[dict[str, str]] = [
    {
        "name": "Qoder",
        "skills_dir": "~/.qoder/skills/",
        "install_pattern": "dir",  # 目录形式: skills/{name}/SKILL.md
    },
    {
        "name": "通义灵码",
        "skills_dir": "~/.lingma/skills/",
        "install_pattern": "dir",
    },
    {
        "name": "Claude Code",
        "skills_dir": "~/.claude/skills/",
        "install_pattern": "dir",
    },
    {
        "name": "Cursor",
        "skills_dir": "~/.cursor/rules/",
        "install_pattern": "file",  # 文件形式: rules/{name}.md
    },
]


@dataclass
class DetectedAgent:
    """检测到的 Coding Agent 信息。"""

    name: str
    skills_dir: Path
    detected: bool
    install_pattern: str  # "dir" | "file"

    def get_install_path(self, skill_name: str) -> Path:
        """获取指定 skill 的安装目标路径。

        Args:
            skill_name: Skill 名称（如 agent-cli-alicloud-workflow）

        Returns:
            安装目标路径
        """
        if self.install_pattern == "file":
            # Cursor 特殊：直接以 .md 文件形式存在于 rules/ 下
            return self.skills_dir / f"{skill_name}.md"
        else:
            # 标准目录形式
            return self.skills_dir / skill_name / "SKILL.md"


def detect_agents(target: str | None = None) -> list[DetectedAgent]:
    """检测本机已安装的 Coding Agent。

    Args:
        target: 指定目标 Coding Agent 名称（qoder|lingma|claude-code|cursor），
                None 表示全部检测

    Returns:
        检测到的 Agent 列表

    Raises:
        ValueError: target 不在支持列表中时抛出
    """
    # target 名称到配置 name 的映射
    target_map: dict[str, str] = {
        "qoder": "Qoder",
        "lingma": "通义灵码",
        "claude-code": "Claude Code",
        "cursor": "Cursor",
    }

    if target is not None and target not in target_map:
        valid_targets = ", ".join(target_map.keys())
        raise ValueError(
            f"不支持的目标 Agent: {target}，建议：使用 {valid_targets} 之一"
        )

    results: list[DetectedAgent] = []

    for config in _AGENT_CONFIGS:
        agent_name = config["name"]

        # 如果指定了 target，只检测该 target
        if target is not None and target_map[target] != agent_name:
            continue

        skills_dir = Path(config["skills_dir"]).expanduser()
        detected = skills_dir.exists()

        results.append(
            DetectedAgent(
                name=agent_name,
                skills_dir=skills_dir,
                detected=detected,
                install_pattern=config["install_pattern"],
            )
        )

    return results
