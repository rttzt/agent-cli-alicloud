"""小红书爆文分析 Agent — 基于 AgentScope + DashScope。

用户输入品类关键词，Agent 分析公开热门笔记的共性要素，输出结构化报告。
"""
import asyncio
import os
import sys

try:
    from agentscope.credential import DashScopeCredential
    from agentscope.formatter import DashScopeChatFormatter
    from agentscope.message import SystemMsg, UserMsg
    from agentscope.model import DashScopeChatModel
    HAS_AGENTSCOPE = True
except ImportError:
    HAS_AGENTSCOPE = False

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


def mock_analyze(keyword: str) -> str:
    """Mock 模式分析（无需 API key，用于开发调试）。"""
    return f"""# 小红书爆文分析报告：{keyword}

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
*本报告基于{keyword}品类公开笔记的通识分析，仅供选题参考。*
"""


def main() -> None:
    """入口函数。"""
    keyword = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    if not keyword:
        print("用法: python -m agent.main <品类关键词>")
        print("示例: python -m agent.main 美妆")
        sys.exit(1)

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


if __name__ == "__main__":
    main()
