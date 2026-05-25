# Evidence Pool v0.1 — Proxy Evidence for the 3 Positioning Pillars

> **状态**：Idea Stage Step 3 / 公开原话 + 创始人观察 + 反向信号汇总
> **日期**：2026-05-21
> **配套**：[01-hypothesis](./01-problem-hypothesis-v0.1.md) · [02-competitive-landscape](./02-competitive-landscape-v0.1.md)
> **重要更新**：本轮搜索发现两个新事实，**已写入第 5 节"危险信号升级"，请创始人在 Step 4 前必须读完**。

---

## 0. 证据强度图例

| 等级 | 含义 |
|---|---|
| 🟢 强 | 来自工程师本人原话 / GitHub Issue / 真实踩坑文章 |
| 🟡 中 | 来自营销稿但暴露了真实痛点 / 自媒体二手陈述 |
| 🔴 反向 | 看似支持其实反过来削弱了我们假设的信号 |
| ⚫ 自证 | 创始人自身/同事观察（私域，可信但有偏） |

---

## 1. 支持 Pillar A —— "商业级对外 Agent" 的痛点真实存在

| 强度 | 原话 / 信号 | 来源 |
|---|---|---|
| 🟢 | 文章标题：**"为什么你的 Agent 任务成功率达标了，却依然无法上线？"** | [阿里云开发者社区](https://developer.aliyun.com/article/1734018) |
| 🟢 | 文中点出 **"假成功陷阱：高任务成功率掩盖逻辑断层与静默失败"** | 同上 |
| 🟢 | 行业论述：**"AI Agent 工程化元年：从 95% 失败率看生产级落地的真正挑战"** | [知乎专栏](https://zhuanlan.zhihu.com/p/2010437035492664715) |
| 🟢 | 文章标题：**"初探：从 0 开始的 AI-Agent 开发踩坑实录"** | [阿里云开发者社区](https://developer.aliyun.com/article/1679487) |
| 🟢 | 峰会描述：**"共识来得太快，踩坑却太碎——GPU/CPU 怎么切、RAG 还值不值得、工具失败率到底卡几位 9、长窗口…"** | [Agentic AI Summit](https://www.bagevent.com/event/9095910/) |
| ⚫ | 创始人口述：**"我们的场景是创建定制的商业级 Agent，跟灵码 create-agent（IDE 内部 agent）不一致"** | Step 2 复盘 |
| ⚫ | R8 自检：**5 位踩过坑的真人，跨研发/解决方案/业务三类岗位** | Step 3 私域 |

**判读**：Pillar A 的"痛是真的、且是工程化级别的痛"已被多条证据支撑。但这 5 位真人**跨三类岗位**这个事实需要你私下回答："5 句话是不是真的指向同一件事？"——若不是，未来要么收窄到一类，要么承认产品其实跨职能。

---

## 2. 支持 Pillar B —— "全生命周期需要前半段" 的痛点

| 强度 | 原话 / 信号 | 来源 |
|---|---|---|
| 🟢 | **"面对如此众多的框架与平台，开发者常常会陷入'选择困难症'。AI Agent 的工具链中没有银弹"** | [53AI 综述](https://www.53ai.com/news/OpenSourceLLM/2026012383275.html) |
| 🟡 | 百炼 MCP 用户评价：**"抓住了当前 AI Agent 开发的一个痛点：易用性和生态整合"** | [知乎问题](https://www.zhihu.com/question/1893408209420665225) |
| 🟢 | "Agent 开发避坑清单"前提："启动项目前必须确认的 10 个问题"——侧面证明**很多人是没确认就开工，导致后续返工** | [CSDN 文章](https://deepseek.csdn.net/6a0275a70a2f6a37c5a95f67.html) |
| ⚫ | 创始人口述：**"环节割裂，从 idea 到设计、coding、部署、观测涉及非常多不同工具，环节之间断裂"** | Step 1 |

**判读**：Pillar B 有公开证据，但**力度比 Pillar A 弱**——大多数公开内容把痛点定位在"部署/上线"而不是"Idea/Design 设计端"。需要警惕：**你的"设计端痛"可能比市场实际更前置**，市场对"设计端"的需求度可能不如"部署端"高。

---

## 3. 支持 Pillar C —— "跨 Coding Agent 友好" 的需求

| 强度 | 原话 / 信号 | 来源 |
|---|---|---|
| 🟢 | Google `agents-cli` 官方明列支持 **Gemini CLI / Claude Code / Codex / Antigravity** 等多种 coding agent，专门写"works seamlessly with…and any other coding agent" | [google/agents-cli](https://github.com/google/agents-cli) |
| ⚫ | 创始人口述：**"在开发的时候用 Qoder，部署的时候部署到百炼，再加上一些开源的开发框架去开发工具"** | Step 1 |
| ⚪ | **公开池子缺乏直接证据** —— 中文社区暂未搜到工程师明确吐槽"我要为多个 coding agent 做适配很麻烦"的原话 | — |

**判读**：⚠️ **这是三根支柱里证据最薄的一根。** Google `agents-cli` 把这个特性当作头号卖点，是间接证据；但中文社区没出现明确的"我有这个痛"的原话。这意味着：
- 要么这个痛存在但**用户表达成了别的词**（比如"切工具上下文好烦"），需要继续找；
- 要么这个痛**还没浮出水面**，是 nice-to-have 不是 must-have；
- 要么这是一个**真正的"先于市场"的洞察**——但这种洞察的失败率是出名的高。

---

## 4. 创始人 R8 自检结果（私域）

| 维度 | 结果 | 我的判读 |
|---|---|---|
| 数量 | 5/8 能具体说出踩坑 | 数量偏弱但 demo 模式可接受 |
| 多样性 | 跨研发 / 解决方案 / 业务 三类岗位 | ⚠ 多样性反而暴露了问题：**ICP 颗粒度可能太粗** |
| 待你私下作业 | 把 5 个人各自的痛各写一句话，看是否指向同一件事 | 强烈建议你做完，否则后续 scope 会发散 |

---

## 5. ⚠️ 危险信号升级（R1 红色警报）

> 这一节是 Step 3 搜索过程中浮出的**新事实**，比 Step 2 看到的更严重。**请你完整读完，然后我们才进 Step 4。**

### 新事实 1：阿里云函数计算 `AgentRun` 已发布

> **官方原话**："AgentRun 是专为 AI Agent 打造的**一站式 Agentic AI 基础设施平台**……以高代码为核心，秉持生态开放……" — [aliyun.com/product/fc/agentrun](https://www.aliyun.com/product/fc/agentrun)

含义：阿里云已经发布了一个**官方"一站式 Agent 基础设施"**，且**"高代码 + 生态开放"**几乎就是你想做的产品形态描述的官方版本。

### 新事实 2：百炼"工作流应用"已存在 ⚠️ **此前的判读是错误的，需澄清**

> 阿里云文档：[百炼工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) ——"在阿里云百炼，通过工作流组合使用大模型、API 和函数计算等节点，可有效降低编码成本"

**【勘误】之前说"百炼工作流应用已覆盖我们的 workflow Skill"是概念错误。** 这两个 `workflow` 完全不在同一层：

| 维度 | **百炼 workflow application** | **我们要做的 `workflow` skill**（同 Google agents-cli） |
|---|---|---|
| 层 | **Runtime 编排器** | **Dev-time 方法论 Skill** |
| 作用对象 | Agent 的**内部执行流**（用户请求来了之后内部如何走分支） | **开发者构建 agent 的过程**（怎么从想法走到能跑的 agent） |
| 形态 | 图形化拖拽节点 | Skill 文档 + 模板 + checklist，被 coding agent 读取后引导对话 |
| 输出 | 一个**可部署的 workflow 应用** | 一套**设计文档 + 项目骨架** |
| 谁消费 | 终端用户的请求 | **Coding Agent**（Claude Code/Qoder/Cursor/...） |
| 类比 | n8n / Dify workflow | 团队 wiki 里的 "How we build agents" 操作手册 |

**所以**：百炼 workflow application **不是竞品也不是覆盖**，它和我们的 `workflow` skill 在不同时间点（runtime vs dev-time）、不同消费者（终端用户 vs coding agent）、不同形态（节点图 vs 文档/模板）做不同的事。**两者并不冲突，甚至互补**——我们的 `workflow` skill 完全可以在产出物里**生成一份百炼 workflow application 的配置**作为 deliverable 之一。

### 这两件事对 MVP 切片的影响（更新后）

| MVP Skill | Step 2 决定 | 现状盘点 | 是否需要重定位 |
|---|---|---|---|
| `bailian-scaffold` | 进 MVP | AgentRun 自带 runtime 项目模板 | ⚠ 角色需澄清——我们做的是面向 coding agent 的 dev-time Skill，不是 runtime 模板生成器 |
| `bailian-workflow` | **进 MVP（核心差异）** | 百炼工作流应用是 **runtime 节点图**，与我们 dev-time skill 不在一层 | ✅ **不冲突，仍是核心差异** |
| `bailian-deploy` | 进 MVP | AgentScope `deploy()` 一键到 FC，AgentRun 一键全套 | ⚠ 需重定位（部署端官方已极致便捷） |
| `bailian-eval` | 进 MVP | 百炼 / AgentScope 都未明确提供完整 eval pipeline | ✅ 仍有差异化 |

### 但同时也找到了**仍存在的窄缝**

🟢 **窄缝 1：跨 Coding Agent Skill 包**
官方 AgentRun 是 SDK + Console，不是面向 coding agent 调用的 Skill 包。**这一条窄缝是我们 Pillar C 的具体落点。**

🟢 **窄缝 2：Eval / 评测端**
百炼提供"流程调试"、AgentScope 提供 sandbox，但**面向商业级对外 Agent 的端到端 evalset + LLM-as-judge + 回归测试管线**目前空白。

🟢 **窄缝 3：从 Idea 到 Scaffold 的"前置工作流"**
所有官方工具都从"已有 idea/已有 spec"开始；**没有官方工具承担"从模糊想法 → CLAUDE.md/AGENTS.md 规范 → scaffold"这一段**。这就是你的 Pillar B。

🟢 **窄缝 4：Issue Bug 池**
AgentScope Runtime 的真实 GitHub Issues：[#443 deploy k8s 报错](https://github.com/agentscope-ai/agentscope-runtime/issues/443)、[#402 race condition](https://github.com/agentscope-ai/agentscope-runtime/issues/402)。**说明官方栈本身仍有摩擦，社区增强层有存在空间。**

---

## 6. 综合判读 → 给 Step 4 的输入

**Idea Stage 现在的总结**（用 Playbook Idea Stage 的三道闸口）：

| 闸口 | 答案 | 说明 |
|---|---|---|
| 1. 问题是真实且具体的吗？ | ✅ Pillar A 强证据；B 中证据；C 弱证据 | 工程化级痛真实存在 |
| 2. 你的方案确实在解决这个问题（不是你最初以为的那个）吗？ | ⚠️ 必须重定位 | 阿里官方已覆盖中后段，必须收窄到三条窄缝里的至少一条 |
| 3. 信号足够支持你开始 MVP 吗？ | ⚠️ 在 demo 模式下足够，但**必须先把 MVP 切片改写** | 不能照原 4 个 Skill 直接开工 |

---

## 7. Step 4 预告

Step 4 = **方案概念 final + Go/Pivot 决策**。你要在三条窄缝里**至少押注一条**作为 MVP 的核心立足点：

- **押注 A**：跨 Coding Agent Skill 包（最贴 Google `agents-cli` 思路）
- **押注 B**：从模糊想法到 scaffold 的前置工作流（Pillar B 的具体化）
- **押注 C**：商业级 Agent 的 eval / 回归测试管线（Pillar A 的具体化）

剩下两条作为辅料，但 MVP 灵魂只能押注 1 条——这就是 Playbook 反复强调的 **"the single core interaction your solution depends on"**。

---

*下一文档：`04-final-concept-and-go-no-go-v0.1.md`*
