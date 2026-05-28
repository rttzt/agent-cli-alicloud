"""小红书公开数据检索工具。

注意：MVP 阶段为 Mock 实现。真实数据源需用户自行配置
（小红书开放平台 API / 第三方数据服务）。

合规红线：
- 仅检索公开可见笔记
- 不爬取私域数据
- 不存储个人 ID
"""
from typing import Any


def fetch_trending_notes(
    keyword: str,
    top_n: int = 20,
) -> list[dict[str, Any]]:
    """检索指定品类的公开热门笔记。

    Args:
        keyword: 品类关键词（如"美妆"、"母婴"）
        top_n: 返回条数，默认 20

    Returns:
        热门笔记元数据列表（标题、互动数、发布时间等）

    Note:
        MVP 阶段返回 Mock 数据。
        接入真实数据源时，替换此函数内部实现即可，接口不变。
    """
    # MVP Mock 数据 — 真实接入时替换此部分
    mock_notes = [
        {
            "title": f"{keyword}好物分享｜这些真的绝了",
            "likes": 15000,
            "collects": 8000,
            "comments": 2300,
            "publish_date": "2026-05-20",
            "content_type": "图文",
        },
        {
            "title": f"新手必看！{keyword}入门指南",
            "likes": 12000,
            "collects": 9500,
            "comments": 1800,
            "publish_date": "2026-05-18",
            "content_type": "视频",
        },
        {
            "title": f"被问了100遍的{keyword}清单，一次说清",
            "likes": 20000,
            "collects": 15000,
            "comments": 3500,
            "publish_date": "2026-05-15",
            "content_type": "图文",
        },
    ]
    return mock_notes[:top_n]
