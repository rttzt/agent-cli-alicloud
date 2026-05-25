"""小红书搜索工具 — 占位实现"""


def search_notes(keyword: str, days: int = 30) -> list[dict[str, str]]:
    """搜索小红书笔记（占位：返回 mock 数据）

    Args:
        keyword: 搜索关键词
        days: 搜索天数范围

    Returns:
        笔记列表
    """
    return [
        {
            "title": f"【{keyword}】超详细测评！这些好物真的绝了",
            "likes": "12000",
            "content_hook": "姐妹们！这篇我真的憋了好久...",
            "tags": f"#{keyword} #好物推荐 #测评",
            "cta": "点赞收藏不迷路，关注我获取更多好物推荐！",
        },
        {
            "title": f"被问了800遍的{keyword}清单，一次全说清",
            "likes": "8500",
            "content_hook": "后台私信都要爆炸了，今天统一回复！",
            "tags": f"#{keyword} #干货分享 #必看",
            "cta": "你们还想看什么品类？评论区告诉我！",
        },
    ]
