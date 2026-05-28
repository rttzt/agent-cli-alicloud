"""读写 agent-cli-manifest.yaml。

# 参考 wiki: 核心概念/项目结构说明.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

MANIFEST_FILENAME = "agent-cli-manifest.yaml"
SCHEMA_VERSION = 1


def write_manifest(
    path: Path,
    name: str,
    template_name: str,
    template_version: str,
    agent_directory: str,
    cli_version: str,
) -> Path:
    """将 manifest 写入指定路径。

    Args:
        path: 目标目录路径
        name: 项目名称
        template_name: 使用的模板名称
        template_version: 模板版本
        agent_directory: Agent 源代码目录
        cli_version: CLI 版本号

    Returns:
        写入的 manifest 文件路径

    Raises:
        ValueError: 路径不存在时抛出
    """
    if not path.is_dir():
        raise ValueError(
            f"目标路径 {path} 不存在或不是目录，建议：先创建目标目录"
        )

    manifest_data: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "name": name,
        "template": {
            "name": template_name,
            "version": template_version,
        },
        "agent_directory": agent_directory,
        "cli_version": cli_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    manifest_path = path / MANIFEST_FILENAME
    manifest_path.write_text(
        yaml.dump(manifest_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return manifest_path


def read_manifest(path: Path) -> dict[str, Any]:
    """读取 manifest 文件并返回解析后的字典。

    Args:
        path: manifest 文件所在目录或文件本身路径

    Returns:
        解析后的 manifest 字典

    Raises:
        FileNotFoundError: manifest 文件不存在时抛出
        ValueError: YAML 解析失败时抛出
    """
    if path.is_dir():
        manifest_path = path / MANIFEST_FILENAME
    else:
        manifest_path = path

    if not manifest_path.exists():
        raise FileNotFoundError(
            f"未找到 {MANIFEST_FILENAME}，建议：先运行 agent-cli init 创建项目"
        )

    content = manifest_path.read_text(encoding="utf-8")
    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        raise ValueError(
            f"{MANIFEST_FILENAME} 格式错误，建议：检查文件是否为合法 YAML"
        )

    return data
