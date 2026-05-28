---
name: agent-cli-alicloud-workflow
description: >
  当用户想要"开发一个 Agent"、"用 AgentScope 构建 Agent"、"设计一个智能体"、
  "从想法到落地"时使用此技能。覆盖 Idea → 澄清 → 设计文档 → 脚手架 → 实现指引
  的完整 dev-workflow。任何 Coding Agent（Qoder / 通义灵码 / Claude Code / Cursor）
  均可消费此技能。
  注意：本项目 workflow 指 dev-time 方法论 Skill，不是百炼 runtime 节点编排器。
metadata:
  author: agent-cli-alicloud
  license: Apache-2.0
  version: 0.2.0
  requires:
    bins:
      - agent-cli
    install: "uvx agent-cli-alicloud setup"
---

# 阿里云 Agent 开发工作流

> **停！** 不要直接写代码。先走完 Phase 0 和 Phase 1，确保你理解用户想做什么、设计文档已生成，再进入脚手架和实现阶段。

**agent-cli-alicloud** 是一个 CLI + Skills 双层架构工具，帮助开发者在 5 分钟内把模糊想法变成结构化设计文档 + 可运行的 AgentScope 项目骨架。

> 安装：`uvx agent-cli-alicloud setup`
> 检查：`agent-cli version`

## Session Continuity & Skill Cross-References

每个阶段开始前，**重新读取**对应 Skill——上下文压缩可能已丢失之前的内容。

| 阶段 | 技能 | 何时加载 |
|------|------|----------|
| 0 — 想法澄清 | 本技能 | 用户提出想法时 |
| 1 — 设计文档 | 本技能 | 澄清完成后 |
| 2 — 脚手架 | `/agent-cli-alicloud-scaffold` | 生成项目结构时 |
| 3 — 实现指引 | 本技能 | 编写代码时 |
| 4 — 评估 | `/agent-cli-alicloud-eval` | 验证 Agent 行为时 |
| 5 — 部署 | `/agent-cli-alicloud-deploy` | 部署到阿里云时 |

---

## Phase 0: Idea Clarification（想法澄清）

> **必须完成**——不澄清就写代码等于猜需求。

当用户说"我想做一个 XXX Agent"时，**不要立即行动**。先问以下 5 个澄清问题，等待用户回答后再继续。用户不回答的，用默认答案兜底。

### 5 个核心澄清问题

| # | 问题 | 默认兜底 |
|---|------|----------|
| 1 | **终端用户是谁？** 这个 Agent 服务什么人？（运营/产品经理/普通消费者/开发者） | 产品经理 |
| 2 | **触发方式？** 用户如何触发 Agent？（对话/定时任务/事件驱动/API 调用） | 对话式 |
| 3 | **输入数据？** Agent 需要什么输入？（用户文本/文件上传/数据库/外部 API） | 用户文本输入 |
| 4 | **输出形态？** Agent 输出什么？（文本回复/结构化报告/文件生成/API 调用） | 文本回复 |
| 5 | **合规边界？** Agent 绝对不能做什么？（数据出境/调用付费 API/生成虚假信息） | 不生成虚假信息、不泄露用户隐私 |

### 澄清后产物

将用户答案整理为一段 **需求摘要**（3-5 句话），确认无误后进入 Phase 1。

---

## Phase 1: Design Documents（设计文档生成）

> **核心产物**：AGENTS.md + scope.md + eval-plan.md

### AGENTS.md 写作要点（5 段结构）

```markdown
# AGENTS.md — {project_name}

## Project Identity
一句话描述：这个 Agent 做什么、给谁用。

## Single Core Interaction
用户与 Agent 的典型一次交互（输入 → 处理 → 输出）。

## Tech Stack
| 层 | 选型 |
|---|---|
| 框架 | AgentScope |
| LLM | 通义千问（DashScope） |
| 部署 | 函数计算 / AgentRun / SAE |

## Data Flow
数据从输入到输出的流转路径，标注哪里调 LLM、哪里调工具。

## Compliance
合规红线清单（来自 Phase 0 第 5 题的答案）。
```

### scope.md 模板

```markdown
# scope.md — {project_name}

## §1 IN（做什么）
- ...

## §2 OUT（不做什么）
- ...

## §3 Feature Amendment 门槛
新增任何功能前必须满足：
1. 不违反 Compliance 红线
2. 不引入新的 LLM 依赖
3. 不扩大数据边界
```

### eval-plan.md 思路（5 维度评分）

| 维度 | 权重 | 说明 |
|------|------|------|
| 功能正确性 | 30% | Agent 是否完成了用户请求 |
| 工具调用准确性 | 25% | 是否调用了正确的工具、参数正确 |
| 安全合规 | 20% | 是否违反合规红线 |
| 响应质量 | 15% | 回复是否清晰、完整、有帮助 |
| 延迟/性能 | 10% | 是否在合理时间内响应 |

---

## Phase 2: Scaffold（脚手架生成）

> 走完 Phase 0 和 Phase 1 后才能执行。

```bash
agent-cli init {project-name} --template agentscope
```

这会生成一个可运行的 AgentScope 项目骨架。详见 `/agent-cli-alicloud-scaffold`。

---

## Phase 3: Implementation Pointers（实现指引）

脚手架生成后，`src/agent/main.py` 是你的主入口。需要做的：

1. **替换 EchoAgent** 为真实的 AgentScope Agent 实现
2. **在 `tools/` 目录**添加自定义工具函数
3. **配置 LLM** — 在 `.env` 中设置 `DASHSCOPE_API_KEY`
4. **运行测试** — `uv run pytest` 确保基础功能正常

### main.py 该写什么

```python
# 1. 导入 AgentScope
from agentscope.agents import DialogAgent
from agentscope.message import Msg

# 2. 初始化 Agent（instruction 来自 AGENTS.md 的 Single Core Interaction）
agent = DialogAgent(
    name="你的 Agent 名称",
    model_config_name="dashscope_chat",
    sys_prompt="你的系统提示词...",
)

# 3. 处理用户消息
response = agent(Msg(name="user", content=user_input, role="user"))
```

---

## Reference: Pillar A/B/C 不许偏离

| 支柱 | 含义 | 红线 |
|------|------|------|
| **A** | 商业级对外发布的 Agent | 不是 IDE 内部 Agent |
| **B** | 覆盖 Idea / Design 前半段 | 不重做 Runtime / 框架 / 部署 |
| **C** | 跨 Coding Agent 友好 | 任意 Coding Agent 都能消费产物 |

---

## When to switch to another skill

| 场景 | 切换到 |
|------|--------|
| 需要生成项目文件结构 | `/agent-cli-alicloud-scaffold` |
| 需要评估 Agent 行为质量 | `/agent-cli-alicloud-eval` |
| 需要部署到阿里云 | `/agent-cli-alicloud-deploy` |
| 需要写 Agent 代码细节 | 回到本技能 Phase 3 |

---

## Related Skills

- `/agent-cli-alicloud-scaffold` — 项目创建与脚手架生成
- `/agent-cli-alicloud-eval` — 评估方法论与评分体系
- `/agent-cli-alicloud-deploy` — 部署到阿里云（函数计算 / AgentRun / SAE）
