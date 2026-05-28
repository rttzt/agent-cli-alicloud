"""xiaohongshu-trend-agent — AgentScope v2.0 兼容的最简 Agent 脚手架。

由 agent-cli init 生成，作为脚手架占位。
真实业务逻辑由用户的 Coding Agent 在 workflow Skill 引导下填充。
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


SYSTEM_PROMPT = "你是一个由 xiaohongshu-trend-agent 驱动的 AI 助手。请根据用户的问题提供有帮助的回答。"


def create_model():
    """创建并配置模型（AgentScope 2.x API）。"""
    if not HAS_AGENTSCOPE:
        return None

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        return None

    credential = DashScopeCredential(api_key=api_key)
    model = DashScopeChatModel(
        credential=credential,
        model="qwen-max",
        stream=False,
        formatter=DashScopeChatFormatter(),
    )
    return model


async def run_agent(model, query: str) -> str:
    """调用真实 LLM 完成回答。"""
    messages = [
        SystemMsg(name="system", content=SYSTEM_PROMPT),
        UserMsg(name="user", content=query),
    ]
    response = await model(messages=messages)
    parts = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts) if parts else str(response.content)


def mock_reply(query: str) -> str:
    """Mock 模式回复（无需 API key，用于开发调试）。"""
    return f"[xiaohongshu-trend-agent] 收到输入: {query}\n（Mock 模式：AgentScope 未安装或未设置 API key）"


def main() -> None:
    """入口函数：uv run python -m agent.main "<你的问题>" 可直接运行。"""
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    if not query:
        print("用法: python -m agent.main <输入内容>")
        print('示例: python -m agent.main "你好"')
        sys.exit(1)

    model = create_model()

    if model is None:
        print(mock_reply(query))
    else:
        result = asyncio.run(run_agent(model, query))
        print(result)


if __name__ == "__main__":
    main()
