"""小红书公开数据检索工具。

支持两种数据源：
1. 从本地 JSON 文件加载（用于测试和演示）
2. Mock 内置数据（兜底）

合规红线：仅检索公开可见笔记，不爬取私域数据，不存储个人 ID。
"""
import json
from pathlib import Path
from typing import Any


# 默认数据文件路径
_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
_DEFAULT_DATA_FILE = _DATA_DIR / "sample_trending_notes.json"


def fetch_trending_notes(
    keyword: str,
    top_n: int = 20,
    data_file: Path | None = None,
) -> list[dict[str, Any]]:
    """检索指定品类的公开热门笔记。

    Args:
        keyword: 品类关键词（如"美妆"、"母婴"）
        top_n: 返回条数，默认 20
        data_file: 自定义数据文件路径（JSON），默认使用内置样本数据

    Returns:
        热门笔记元数据列表
    """
    # 优先从数据文件加载
    source_file = data_file or _DEFAULT_DATA_FILE
    if source_file.exists():
        try:
            data = json.loads(source_file.read_text(encoding="utf-8"))
            categories = data.get("categories", {})
            # 精确匹配或模糊匹配
            notes = categories.get(keyword, [])
            if not notes:
                # 尝试模糊匹配
                for cat_name, cat_notes in categories.items():
                    if keyword in cat_name or cat_name in keyword:
                        notes = cat_notes
                        break
            if notes:
                return notes[:top_n]
        except (json.JSONDecodeError, KeyError):
            pass

    # 兜底 Mock 数据
    mock_notes = [
        {
            "note_id": f"fallback_{i}",
            "title": f"{keyword}好物分享｜第{i}期",
            "author": f"创作者{i}",
            "likes": 10000 + i * 1000,
            "collects": 5000 + i * 500,
            "comments": 1000 + i * 100,
            "publish_date": "2026-05-20",
            "content_type": "图文",
            "tags": [keyword],
        }
        for i in range(1, min(top_n, 5) + 1)
    ]
    return mock_notes[:top_n]
