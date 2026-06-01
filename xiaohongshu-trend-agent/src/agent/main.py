"""小红书爆文分析 Agent — 基于 AgentScope + DashScope。

用户输入品类关键词，Agent 分析公开热门笔记的共性要素，输出结构化报告。
"""
import asyncio
import os
import sys
from pathlib import Path

# 自动加载 .env 文件（如果存在）
_env_file = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

from agent.tools.trend_fetcher import fetch_trending_notes

try:
    from agentscope.credential import DashScopeCredential
    from agentscope.formatter import DashScopeChatFormatter
    from agentscope.message import SystemMsg, UserMsg
    from agentscope.model import DashScopeChatModel
    HAS_AGENTSCOPE = True
except ImportError:
    HAS_AGENTSCOPE = False

try:
    from agentscope.message import AssistantMsg  # type: ignore
    HAS_ASSISTANT_MSG = True
except ImportError:
    HAS_ASSISTANT_MSG = False

# 已知品类（用于 Mock 模式下的意图识别）
_KNOWN_CATEGORIES = ["美妆", "母婴", "家居", "健身", "美食", "数码", "穿搭", "宠物", "旅行"]

# 追问意图关键词
_FOLLOWUP_INTENTS = {
    "标题": "title",
    "封面": "cover",
    "配色": "cover",
    "内容": "content",
    "结构": "content",
    "互动": "interaction",
    "评论": "interaction",
    "收藏": "interaction",
}

SYSTEM_PROMPT = """你是一个专业的小红书内容分析师，帮助个人博主分析爆文规律。

当用户给出品类关键词时，你需要：
1. 分析该品类下小红书爆文的共性特征
2. 从以下维度进行拆解：
   - 标题模式（常用句式、关键词、情绪词）
   - 封面规律（构图、配色、文字排版）
   - 内容结构（开头钩子、正文框架、结尾引导）
   - 互动特征（评论区话题、收藏动机）
3. 输出结构化的爆文要素拆解报告

合规要求：
- 仅分析公开可见内容
- 不涉及私域数据
- 不生成虚假数据
- 分析基于行业通识和公开案例
"""


def create_model():
    """创建并配置 DashScope 聊天模型（AgentScope 2.x API）。"""
    if not HAS_AGENTSCOPE:
        print("警告：AgentScope 未安装，使用 Mock 模式运行")
        return None

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("警告：未设置 DASHSCOPE_API_KEY，使用 Mock 模式运行")
        return None

    credential = DashScopeCredential(api_key=api_key)
    model = DashScopeChatModel(
        credential=credential,
        model="qwen-max",
        stream=False,
        formatter=DashScopeChatFormatter(),
    )
    return model


async def run_real_analysis(model, keyword: str) -> str:
    """调用真实 LLM 完成爆文分析。"""
    messages = [
        SystemMsg(name="system", content=SYSTEM_PROMPT),
        UserMsg(
            name="user",
            content=f"请帮我分析小红书「{keyword}」品类的爆文规律，输出结构化的要素拆解报告。",
        ),
    ]
    response = await model(messages=messages)
    # response.content 在 AgentScope 2.x 是 ContentBlock 列表，提取所有 text
    parts = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts) if parts else str(response.content)


def _summarize_notes(notes: list[dict]) -> str:
    """将笔记数据摘要为可读文本。"""
    lines = []
    for i, note in enumerate(notes[:5], 1):
        title = note.get("title", "未知")
        likes = note.get("likes", 0)
        collects = note.get("collects", 0)
        comments = note.get("comments", 0)
        content_type = note.get("content_type", "图文")
        lines.append(
            f"  {i}. 「{title}」— {content_type} | "
            f"赞{likes:,} 藏{collects:,} 评{comments:,}"
        )
    return "\n".join(lines)


def mock_analyze(keyword: str) -> str:
    """Mock 模式分析（无需 API key，用于开发调试）。"""
    notes = fetch_trending_notes(keyword)
    notes_summary = _summarize_notes(notes)

    # 统计数据
    total = len(notes)
    avg_likes = sum(n.get("likes", 0) for n in notes) // max(total, 1)
    avg_collects = sum(n.get("collects", 0) for n in notes) // max(total, 1)
    video_count = sum(1 for n in notes if n.get("content_type") == "视频")
    image_count = total - video_count

    # 提取高频标签
    tag_counter: dict[str, int] = {}
    for note in notes:
        for tag in note.get("tags", []):
            tag_counter[tag] = tag_counter.get(tag, 0) + 1
    top_tags = sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)[:6]
    tags_str = "、".join(f"#{t[0]}" for t in top_tags)

    return f"""# 小红书爆文分析报告：{keyword}

## 数据概览
- 分析样本：{total} 篇热门笔记
- 平均点赞：{avg_likes:,}
- 平均收藏：{avg_collects:,}
- 内容形式：图文 {image_count} 篇 / 视频 {video_count} 篇
- 高频标签：{tags_str}

## TOP5 爆文
{notes_summary}

## 标题模式
- 数字型：「{keyword}必买的 10 个好物」
- 反问型：「为什么你的{keyword}总是踩雷？」
- 种草型：「闺蜜推荐的{keyword}神器，真的绝了」
- 情绪词高频：绝了、救命、yyds、真香

## 封面规律
- 构图：产品平铺 / 对比图 / 使用前后
- 配色：高饱和暖色调为主（粉、橘、奶白）
- 文字：大字标题 + 关键数据标注
- 人物出镜率约 60%

## 内容结构
- 开头钩子：痛点共鸣 / 成果展示（前 3 秒决定停留）
- 正文框架：问题 → 方案 → 使用体验 → 对比
- 结尾引导：「你们还想看什么品类？评论区告诉我」

## 互动特征
- 高赞评论以「求链接」「已下单」为主
- 收藏动机：实用清单型内容收藏率最高
- 互动峰值时段：20:00-22:00

---
*本报告基于 {total} 篇「{keyword}」品类公开笔记的数据分析，仅供选题参考。*
"""


def run_single(keyword: str) -> None:
    """单次模式：分析指定品类后退出（向后兼容）。"""
    print(f"正在分析「{keyword}」品类的爆文规律...\n")

    model = create_model()

    if model is None:
        # Mock 模式
        result = mock_analyze(keyword)
        print(result)
    else:
        # 真实模式
        result = asyncio.run(run_real_analysis(model, keyword))
        print(result)


def _detect_category(text: str) -> str | None:
    """从文本中提取品类关键词。"""
    for cat in _KNOWN_CATEGORIES:
        if cat in text:
            return cat
    return None


def _detect_followup(text: str) -> str | None:
    """识别追问意图，返回意图标签。"""
    for kw, tag in _FOLLOWUP_INTENTS.items():
        if kw in text:
            return tag
    return None


def chat_mock(user_input: str, state: dict) -> str:
    """Mock 对话模式。

    根据用户输入判断意图：
    - 包含品类关键词 → 调用 fetch_trending_notes 给出完整分析
    - 追问（标题/封面/内容/互动）→ 基于上一次品类回答
    - 其他 → 提示用法
    """
    # 1) 品类意图：直接给完整分析
    category = _detect_category(user_input)
    if category:
        state["last_category"] = category
        return mock_analyze(category)

    # 2) 追问意图：基于上下文
    followup = _detect_followup(user_input)
    last = state.get("last_category")
    if followup and last:
        return _mock_followup_answer(last, followup)
    if followup and not last:
        return "我还不知道你想聊哪个品类，请先告诉我（如：美妆 / 母婴 / 家居）。"

    # 3) 其他
    return (
        "我可以帮你分析小红书爆文规律。试试：\n"
        "  • 输入品类关键词（如：美妆 / 母婴 / 家居）\n"
        "  • 用自然语言提问（如：帮我分析母婴品类的爆文）\n"
        "  • 追问细节（如：标题怎么写？封面什么配色？）\n"
        "  • 输入 exit / quit / 退出 结束对话"
    )


def _mock_followup_answer(category: str, intent: str) -> str:
    """Mock 模式下的追问回答（基于通用规律 + 品类语境）。"""
    if intent == "title":
        return (
            f"## 「{category}」标题模式追问\n"
            f"- 数字型：「{category}必买的 10 个好物」\n"
            f"- 反问型：「为什么你的{category}总是踩雷？」\n"
            f"- 种草型：「闺蜜推荐的{category}神器，真的绝了」\n"
            f"- 高频情绪词：绝了 / 救命 / yyds / 真香\n"
            f"建议字数控制在 16~22 字，前 8 字承载核心钩子。"
        )
    if intent == "cover":
        return (
            f"## 「{category}」封面规律追问\n"
            f"- 配色：高饱和暖色调为主（粉、橘、奶白），与{category}调性贴合\n"
            f"- 构图：产品平铺 / 对比图 / 使用前后\n"
            f"- 文字：大字标题 + 关键数据标注（如「省 50%」）\n"
            f"- 人物出镜率约 60%，真实感优于摆拍"
        )
    if intent == "content":
        return (
            f"## 「{category}」内容结构追问\n"
            f"- 开头钩子：痛点共鸣 / 成果展示（前 3 秒决定停留）\n"
            f"- 正文框架：问题 → 方案 → 体验 → 对比\n"
            f"- 结尾引导：「你们还想看什么{category}相关内容？评论区告诉我」"
        )
    if intent == "interaction":
        return (
            f"## 「{category}」互动特征追问\n"
            f"- 高赞评论以「求链接」「已下单」为主\n"
            f"- 收藏动机：实用清单型内容收藏率最高\n"
            f"- 互动峰值时段：20:00-22:00"
        )
    return f"暂未覆盖该追问维度，可以试试问标题 / 封面 / 内容 / 互动。"


async def _chat_with_llm_async(model, history: list) -> str:
    """异步调用 LLM，返回回复文本。"""
    response = await model(messages=history)
    parts = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts) if parts else str(response.content)


def chat_with_llm(model, user_input: str, history: list) -> str:
    """使用真实 LLM 进行对话，保留上下文。

    history 是 AgentScope 消息对象列表（首项为 SystemMsg）。
    """
    history.append(UserMsg(name="user", content=user_input))
    reply = asyncio.run(_chat_with_llm_async(model, history))
    # 将 AI 回复加入历史，便于下一轮上下文
    if HAS_ASSISTANT_MSG:
        history.append(AssistantMsg(name="assistant", content=reply))
    else:
        # 退化：以 UserMsg 形式注入，仅作上下文占位（极少触发）
        history.append(UserMsg(name="assistant", content=f"[上一轮我的回答]\n{reply}"))
    return reply


def run_chat() -> None:
    """交互式对话模式。"""
    print("=" * 50)
    print("  小红书爆文分析 Agent — 对话模式")
    print("=" * 50)
    print()
    print("你可以：")
    print("  • 输入品类关键词直接分析（如：美妆）")
    print("  • 用自然语言提问（如：帮我分析母婴品类的爆文规律）")
    print("  • 追问细节（如：标题一般怎么写？）")
    print("  • 输入 exit / quit / 退出 结束对话")
    print()

    model = create_model()
    # LLM 历史：以 SystemMsg 起手；Mock 历史：用 dict 跟踪上下文
    if model is not None and HAS_AGENTSCOPE:
        history: list = [SystemMsg(name="system", content=SYSTEM_PROMPT)]
    else:
        history = []
    mock_state: dict = {}

    while True:
        try:
            user_input = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q") or user_input == "退出":
            print("再见！")
            break

        if model is not None:
            try:
                response = chat_with_llm(model, user_input, history)
            except Exception as e:  # 网络/鉴权失败时优雅降级
                response = f"[LLM 调用失败，已降级 Mock] {e}\n\n" + chat_mock(
                    user_input, mock_state
                )
        else:
            response = chat_mock(user_input, mock_state)

        print(f"\nAgent> {response}\n")


def main() -> None:
    """入口函数。

    - 带参数：单次模式（向后兼容），如 `python -m agent.main 美妆`
    - 不带参数：进入交互式对话模式
    """
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
        run_single(keyword)
    else:
        run_chat()


if __name__ == "__main__":
    main()
