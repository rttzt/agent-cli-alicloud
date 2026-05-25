# Final Concept & Go Decision v0.1

> **状态**：Idea Stage Step 4 / 决策：**Go (Demo Mode)** / 收口文档
> **日期**：2026-05-21
> **配套**：[01-hypothesis](./01-problem-hypothesis-v0.1.md) · [02-competitive-landscape](./02-competitive-landscape-v0.1.md) · [03-evidence-pool](./03-evidence-pool-v0.1.md)

---

## 1. 一句话产品概念（v0.1 Final）

> **`agent-cli-alicloud` 是一个开源 CLI + Skill 包，让任意 Coding Agent（Qoder / 通义灵码 / Claude Code / Cursor / Gemini CLI / Codex）能在 5 分钟内把一句模糊的 Agent 想法，转换成一套结构化的设计文档（AGENTS.md / CLAUDE.md / Scope Doc / 评测计划）+ 可被 AgentScope / AgentRun / 百炼直接消费的脚手架。**

**它不做什么**（防止零摩擦 scope creep）：
- ❌ 不重做 Agent 框架（直接生成 AgentScope/LangGraph 兼容代码）
- ❌ 不重做 Runtime / Sandbox（直接复用 AgentRun / FC / SAE）
- ❌ 不重做 **runtime 图形化 workflow 编排**（百炼工作流应用 / Dify / n8n 是 runtime 节点图，那是 agent 跑起来后内部那条流水线，**不是**我们做的 dev-time 工作流）
- ❌ 不绑定单一 Coding Agent / 单一 IDE

**它做的"workflow"是什么**（关键澄清）：
我们的 `workflow` 是 **dev-time 方法论 Skill**（同 Google `agents-cli` 的 `workflow` skill 概念）：
被 coding agent 读取后，引导开发者**从一句模糊想法 → 澄清问题 → 设计文档 → 脚手架**这个**造物过程**——它的消费者是 Coding Agent，不是终端用户的请求。
**它和百炼 workflow application 不在同一层、不冲突、甚至互补**：我们的产出物可以包含一份百炼 workflow application 的初始配置。

---

## 2. Idea Stage 三道闸口 Final 答卷

| 闸口 | 答卷 |
|---|---|
| 1. 问题真实且具体？ | ✅ "Agent 上线前的设计/规范/脚手架阶段普遍混乱"——证据见 03 文档 Pillar A/B |
| 2. 你的方案在解决真问题？ | ✅ Demo 版押注窄缝 3：填补"模糊想法 → 可被官方栈消费的 spec/scaffold"这一空白段 |
| 3. 信号足够支持开始 MVP？ | ✅ Demo 模式下足够。商业化版本仍需访谈 |

**Go decision**：在**严格的"窄缝 3 + Demo 学习"约束下** Go。

---

## 3. 单一核心交互（The Single Core Interaction）

> 这就是 Playbook 第 14 页的 "the single core interaction your solution depends on"——MVP 必须围绕它，**只**围绕它。

```
$ agent-cli init "我想做一个能帮品牌方分析小红书爆文的 Agent"

[1/4] 提问澄清    → 提 5 个关键澄清问题（用户/触发/输入/输出/合规）
[2/4] 文档生成    → 生成 AGENTS.md + CLAUDE.md + scope.md + eval-plan.md
[3/4] 脚手架     → 生成 AgentScope 兼容的 Python/Java 项目骨架
[4/4] 推送到 IDE  → 自动写入当前目录,任意 Coding Agent 接手即可继续编码
```

**核心承诺**：从"一句模糊想法"到"任意 Coding Agent 能接着写代码的状态"，**5 分钟**。

---

## 4. ICP 与 R8 警示

| ICP（v0.2 收窄） | "在阿里云上做商业级对外 Agent 的研发/解决方案/业务工程师，需要快速从想法转入可被 coding agent 接手的状态" |
|---|---|
| 私域 5 人样本 | 跨研发/解决方案/业务三类——需在 MVP-3 hands-on 试用阶段验证：他们在窄缝 3 上的痛是否真的指向同一件事 |
| R8 仍未关闭 | 创始人需私下完成"5 句话痛点是否同向"的自答；若 ≥3 句不同向，MVP-3 之后必须收窄 ICP |

---

## 5. R1 持续监控 watchlist

为了避免 MVP 期间被官方"长出来"碾压，每两周扫一次：

- AgentScope release notes（github.com/agentscope-ai/agentscope）
- AgentRun / 函数计算 release notes
- 百炼 ModelStudio 更新
- 通义灵码 Qoder CN 智能体更新（特别是 `create-agent`）

⚠ **触发 Pivot 的条件**：上述任何一家明确推出"模糊想法 → 设计文档 → 脚手架"的端到端工具，立即重评估。

---

## 6. 出 Idea Stage 进 MVP Stage 的硬纪律（demo 版）

> 这一节是创始人对自己的**契约**。MVP 阶段每次诱惑出现时回来读一遍。

1. **Qoder 开工前必须先写 `AGENTS.md` + Scope Doc**——否则不开第一行代码（Playbook 第 17 页）
2. **MVP 仅做单一核心交互**——其它 3 条窄缝（Skill 跨适配、Eval、回归测试）一律进 Roadmap
3. **每一次 Qoder Session 结束都要更新 `AGENTS.md`** —— 防止 agentic 技术债累积（Playbook 第 16 页）
4. **公开发布前必须做一次 Claude/Qoder 安全审查**——Demo 也不能留明显漏洞
5. **本 demo 收尾标志**：≥10 个 GitHub Star + ≥3 位试用者反馈（≥1 位写文字反馈）+ 一篇创始人复盘文 = "Demo PMF"

---

## 7. 进入 MVP Stage 路线图（4 步）

```
MVP-1 [当前]   写 AGENTS.md + Scope Doc + 拍板技术栈
MVP-2          Qoder 构建 lightweight prototype（仅核心交互的最小可跑）
MVP-3          3-5 位 hands-on 试用 + 反馈记录 + 同向性检验
MVP-4          GitHub 指标框架 + 安全审查 + 公开发布前检查清单
```

---

*Idea Stage 完。下一文档：`mvp/01-AGENTS.md`*
