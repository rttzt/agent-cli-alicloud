"""LLM 调用层 — 集中管理 Prompt 常量与模型调用逻辑"""

import json
import os

# ---------------------------------------------------------------------------
# MOCK_MODE: 无 API Key 时自动启用 Mock 模式
# ---------------------------------------------------------------------------
MOCK_MODE: bool = not bool(os.environ.get("DASHSCOPE_API_KEY"))

# ---------------------------------------------------------------------------
# Prompt 常量（项目规则：所有 Prompt 集中在此，不散落业务模块）
# ---------------------------------------------------------------------------

SYSTEM_PROMPT: str = (
    "你是一位专业的 AI Agent 架构师，擅长将模糊的产品想法转化为清晰的技术设计文档。"
)

CLARIFICATION_PROMPT: str = """基于以下 Agent 想法，生成 5 个澄清问题，每个问题附带一个合理的默认答案。

问题必须覆盖以下 5 个固定大类：
1. 终端用户：这个 Agent 的目标用户是谁？
2. 触发方式：用户如何触发/启动这个 Agent？
3. 数据来源：Agent 需要什么数据输入？来源是什么？
4. 输出形态：Agent 的输出是什么形式？
5. 合规要求：有什么数据安全或合规方面的要求？

请严格按以下 JSON 格式输出：
{
  "questions": [
    {
      "category": "终端用户",
      "question": "...",
      "default_answer": "..."
    },
    ...共 5 个
  ]
}

用户的 Agent 想法：
{idea}"""

DOCUMENT_GEN_PROMPT: str = """基于以下 Agent 想法和澄清问答，生成项目设计文档所需的结构化数据。

请严格按以下 JSON 格式输出：
{
  "project_name": "项目英文名（小写连字符）",
  "project_name_cn": "项目中文名",
  "one_liner": "一句话描述项目",
  "icp": "目标用户画像",
  "what_we_dont_do": ["不做的事情1", "不做的事情2", "不做的事情3"],
  "core_interaction": "用户从输入到输出的全流程描述",
  "tech_stack": {
    "language": "Python",
    "framework": "框架名",
    "llm": "LLM 服务",
    "data_source": "数据来源"
  },
  "data_flow": ["步骤1", "步骤2", "步骤3", "步骤4", "步骤5"],
  "compliance": ["合规要求1", "合规要求2"],
  "scope_in": ["做什么1", "做什么2", "做什么3"],
  "scope_out": ["不做什么1", "不做什么2", "不做什么3"],
  "eval_samples": [
    {"input": "输入示例", "expected_dimensions": ["维度1", "维度2"]},
    ...共 5 个
  ],
  "eval_dimensions": ["评分维度1", "评分维度2", "评分维度3", "评分维度4", "评分维度5"],
  "next_steps": [
    {"task": "任务描述", "detail": "详细说明"},
    ...共 3 个
  ]
}

Agent 想法：{idea}

澄清问答：
{clarification}"""

# ---------------------------------------------------------------------------
# Mock 数据（小红书爆文分析 Agent 场景）
# ---------------------------------------------------------------------------

_MOCK_CLARIFICATION: str = json.dumps(
    {
        "questions": [
            {
                "category": "终端用户",
                "question": "这个 Agent 的目标用户是谁？",
                "default_answer": "品牌方运营人员和内容策划，需要快速了解小红书内容趋势",
            },
            {
                "category": "触发方式",
                "question": "用户如何触发/启动这个 Agent？",
                "default_answer": "通过输入品类关键词或竞品账号名称来触发分析",
            },
            {
                "category": "数据来源",
                "question": "Agent 需要什么数据输入？来源是什么？",
                "default_answer": (
                    "小红书公开笔记数据，通过小红书搜索 API 或第三方爬虫获取"
                    "（用户自行配置 API Key）"
                ),
            },
            {
                "category": "输出形态",
                "question": "Agent 的输出是什么形式？",
                "default_answer": (
                    "结构化的爆文要素拆解报告（标题、封面、钩子、标签、CTA）"
                    "+ 选题建议清单"
                ),
            },
            {
                "category": "合规要求",
                "question": "有什么数据安全或合规方面的要求？",
                "default_answer": (
                    "仅采集公开可见内容，不存储用户个人 ID，"
                    "不进行任何形式的数据倒卖"
                ),
            },
        ]
    },
    ensure_ascii=False,
)

_MOCK_DOCUMENT: str = json.dumps(
    {
        "project_name": "xiaohongshu-trend-agent",
        "project_name_cn": "小红书爆文分析 Agent",
        "one_liner": "帮助品牌方运营人员快速分析小红书爆文趋势，拆解爆款要素并生成选题建议",
        "icp": "品牌方运营人员和内容策划，每周需要产出 3-5 篇小红书内容",
        "what_we_dont_do": [
            "不做自动发布——只提供分析和建议，不代替用户发布内容",
            "不做账号管理——不涉及小红书账号的登录、运营或数据管理",
            "不做付费投放优化——不涉及广告投放策略或 ROI 分析",
        ],
        "core_interaction": (
            "用户输入品类关键词（如'美妆'）或竞品账号 → Agent 检索近期爆文"
            " → 拆解标题/封面/钩子/标签/CTA 五要素 → 输出趋势报告 + 3 条选题建议"
        ),
        "tech_stack": {
            "language": "Python",
            "framework": "AgentScope",
            "llm": "DashScope Qwen",
            "data_source": "小红书搜索 API / 第三方爬虫",
        },
        "data_flow": [
            "用户输入品类关键词或竞品账号",
            "Agent 调用搜索 API 检索近 30 天爆文（点赞 > 1000）",
            "对每篇爆文提取标题、封面、正文钩子、标签、CTA",
            "LLM 分析共性模式，拆解为五要素趋势报告",
            "生成 3 条可执行的选题建议，输出结构化报告",
        ],
        "compliance": [
            "仅采集小红书公开可见内容，不爬取私密或仅粉丝可见内容",
            "不存储笔记作者的个人 ID、手机号等隐私信息",
        ],
        "scope_in": [
            "基于关键词/账号的爆文检索与数据采集",
            "爆文五要素（标题/封面/钩子/标签/CTA）自动拆解",
            "趋势分析报告生成 + 选题建议",
        ],
        "scope_out": [
            "小红书内容自动发布",
            "账号登录与粉丝管理",
            "付费投放与广告优化",
        ],
        "eval_samples": [
            {
                "input": "美妆品类近7天爆文",
                "expected_dimensions": ["召回相关性", "要素拆解准确度"],
            },
            {
                "input": "竞品账号@完美日记官方",
                "expected_dimensions": ["账号识别准确性", "内容覆盖率"],
            },
            {
                "input": "母婴品类 TOP10 笔记",
                "expected_dimensions": ["排序准确性", "要素完整度"],
            },
            {
                "input": "护肤成分党内容趋势",
                "expected_dimensions": ["趋势识别准确性", "选题可行性"],
            },
            {
                "input": "零食品类爆文标题分析",
                "expected_dimensions": ["标题要素提取", "模式归纳质量"],
            },
        ],
        "eval_dimensions": [
            "召回相关性",
            "要素拆解准确度",
            "选题建议可行性",
            "合规清洁度",
            "端到端时延",
        ],
        "next_steps": [
            {
                "task": "替换数据源占位实现",
                "detail": (
                    "替换 tools/xhs_search.py 占位实现，接入真实的小红书数据源"
                    "（搜索 API 或第三方爬虫），配置 API Key 环境变量"
                ),
            },
            {
                "task": "实现爆文要素拆解",
                "detail": (
                    "在 src/agent/main.py 里加入'爆文要素拆解'的 ReAct 循环，"
                    "覆盖标题/封面/钩子/标签/CTA 五要素分析"
                ),
            },
            {
                "task": "编写评测套件",
                "detail": (
                    "参考 eval-plan.md 编写评测数据集，放入 tests/eval/ 目录，"
                    "运行 pytest tests/eval/ 验证各维度达标"
                ),
            },
        ],
    },
    ensure_ascii=False,
)

# ---------------------------------------------------------------------------
# 公共 API
# ---------------------------------------------------------------------------


def call_llm(prompt: str, system: str = "") -> str:
    """调用 LLM 获取响应，无 API Key 时自动使用 Mock 模式。

    Args:
        prompt: 用户 prompt
        system: 系统 prompt（可选，默认使用 SYSTEM_PROMPT）

    Returns:
        LLM 响应文本
    """
    if MOCK_MODE:
        return _mock_response(prompt)
    return _real_call(prompt, system)


def _real_call(prompt: str, system: str) -> str:
    """真实 DashScope 调用（OpenAI 兼容接口）"""
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("DASHSCOPE_API_KEY", ""),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": system or SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def _mock_response(prompt: str) -> str:
    """根据 prompt 内容返回对应的 mock 数据。

    - 包含澄清问题特征 → 返回澄清问题 mock
    - 包含文档生成特征 → 返回文档数据 mock
    """
    if "澄清问题" in prompt or "clarification" in prompt.lower():
        return _MOCK_CLARIFICATION
    return _MOCK_DOCUMENT
