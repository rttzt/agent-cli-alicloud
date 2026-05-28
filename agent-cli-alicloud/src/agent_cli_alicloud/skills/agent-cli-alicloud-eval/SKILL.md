---
name: agent-cli-alicloud-eval
description: >
  当用户想要"评估 Agent"、"测试 Agent 质量"、"验证 Agent 行为"、
  "写评估用例"、"调试评估分数"时使用此技能。覆盖 AgentScope eval harness
  语境下的评估方法论、5 维度评分体系和评估迭代循环。
  不用于编写 Agent 代码（使用 agent-cli-alicloud-workflow）或
  部署操作（使用 agent-cli-alicloud-deploy）。
metadata:
  author: agent-cli-alicloud
  license: Apache-2.0
  version: 0.2.0
  requires:
    bins:
      - agent-cli
    install: "uvx agent-cli-alicloud setup"
---

# 阿里云 Agent 评估指南

> **依赖：** `agent-cli`（`uvx agent-cli-alicloud setup` 安装）

> **评估是最重要的阶段。** 没有评估就上线等于盲人开车。

---

## 5 维度评分体系

| 维度 | 权重 | 说明 | 评判方式 |
|------|------|------|----------|
| **功能正确性** | 30% | Agent 是否完成了用户请求的核心任务 | LLM-as-Judge / 规则匹配 |
| **工具调用准确性** | 25% | 是否调用了正确的工具、参数是否正确、调用顺序是否合理 | Trajectory 匹配 |
| **安全合规** | 20% | 是否违反合规红线（来自 AGENTS.md Compliance） | 规则检查 + LLM 判断 |
| **响应质量** | 15% | 回复是否清晰、完整、格式正确、有帮助 | Rubric-based 评分 |
| **延迟/性能** | 10% | 是否在合理时间内响应（建议 < 10s） | 计时器 |

---

## 评估迭代循环（Eval-Fix Loop）

评估是迭代的。分数不达标时，诊断原因、修复、重跑——不要只报告失败。

### 迭代步骤

1. **从小处开始**：先写 1-2 个评估用例，不要一上来就写全套
2. **运行评估**：执行评估脚本
3. **读分数**：找出什么失败了、为什么失败
4. **修代码**：调整 prompt、工具逻辑、instruction
5. **重跑评估**：验证修复有效
6. **重复 3-5** 直到通过
7. **再加新用例**：扩大覆盖范围

**预期 5-10+ 次迭代。** 这是正常的——每次迭代让 Agent 更好。

### 避免的捷径

| 捷径 | 为什么失败 |
|------|-----------|
| "降低阈值让评估通过" | 掩盖真实问题，Agent 质量不会提升 |
| "这个用例太不稳定，跳过" | 不稳定说明 Agent 行为不确定，应修复而非忽略 |
| "只需调评估用例，不调 Agent" | 如果总在调期望输出，说明 Agent 有行为问题 |

---

## 评估用例设计

### 用例结构

```python
# 评估用例示例
eval_case = {
    "id": "search_test_01",
    "input": "帮我分析最近的小红书美妆趋势",
    "expected_tools": ["search_trends", "analyze_data"],
    "expected_output_contains": ["趋势", "品类"],
    "compliance_check": ["不推荐违禁产品", "不生成虚假数据"],
    "max_latency_seconds": 10,
}
```

### 用例覆盖建议

| 类型 | 数量 | 目的 |
|------|------|------|
| Happy path（正常路径） | 3-5 | 验证核心功能 |
| Edge case（边界情况） | 2-3 | 验证异常处理 |
| Safety（安全用例） | 2-3 | 验证合规红线 |
| Performance（性能用例） | 1-2 | 验证响应时间 |

---

## 评分失败诊断

| 失败症状 | 原因 | 修复方法 |
|---------|------|----------|
| 功能正确性低 | Agent 理解错误或 instruction 不清晰 | 优化 system prompt |
| 工具调用错误 | 工具描述不清晰或 Agent 选错工具 | 完善 tool description |
| 安全违规 | instruction 中缺少约束 | 添加负面约束到 prompt |
| 响应质量低 | 回复过于简略或格式混乱 | 在 instruction 中明确输出格式 |
| 延迟过高 | 工具调用过多或 LLM 请求过大 | 减少不必要的工具调用、缩短 context |

---

## AgentScope Eval Harness 集成

在 AgentScope 框架下进行评估：

```python
"""评估脚本示例 — 用于验证 Agent 行为。"""
import time
from agent.main import EchoAgent, Msg  # 替换为你的 Agent


def evaluate_case(agent, input_text: str, expected_content: str) -> dict:
    """评估单个用例。"""
    start = time.time()
    msg = Msg(name="user", content=input_text, role="user")
    response = agent.reply(msg)
    latency = time.time() - start

    return {
        "passed": expected_content in response.content,
        "latency": latency,
        "response": response.content,
    }


def run_eval():
    """运行评估套件。"""
    agent = EchoAgent(name="test-agent")
    cases = [
        {"input": "你好", "expected": "你好"},
        {"input": "分析趋势", "expected": "分析趋势"},
    ]

    results = []
    for case in cases:
        result = evaluate_case(agent, case["input"], case["expected"])
        results.append(result)
        status = "✓" if result["passed"] else "✗"
        print(f"{status} input='{case['input']}' latency={result['latency']:.2f}s")

    passed = sum(1 for r in results if r["passed"])
    print(f"\n总计: {passed}/{len(results)} 通过")


if __name__ == "__main__":
    run_eval()
```

---

## 评估 vs 单元测试

| | 单元测试 (`pytest`) | Agent 评估 |
|---|---|---|
| 测什么 | 代码正确性（导入、类型、API 契约） | Agent 行为（回复质量、工具使用、安全） |
| 确定性 | 高（输入→输出固定） | 低（LLM 输出不确定） |
| 运行方式 | `uv run pytest` | 评估脚本 |
| 适用场景 | 验证工具函数、数据处理 | 验证对话行为、端到端流程 |

**规则：** 不要写 pytest 断言 LLM 输出内容。LLM 输出不确定——用评估代替。

---

## When to switch to another skill

| 场景 | 切换到 |
|------|--------|
| 需要从头设计 Agent | `/agent-cli-alicloud-workflow` |
| 需要创建/重建项目骨架 | `/agent-cli-alicloud-scaffold` |
| 评估通过，准备部署 | `/agent-cli-alicloud-deploy` |

---

## Related Skills

- `/agent-cli-alicloud-workflow` — 开发工作流、想法澄清、设计文档生成
- `/agent-cli-alicloud-scaffold` — 项目创建与脚手架生成
- `/agent-cli-alicloud-deploy` — 部署到阿里云（函数计算 / AgentRun / SAE）
