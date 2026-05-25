# Competitive Landscape v0.1 — Alicloud Agent CLI

> **状态**：Idea Stage Step 2 / 已扫描 / 三根定位支柱待 Step 3 证据验证
> **日期**：2026-05-21
> **配套文档**：[01-problem-hypothesis-v0.1.md](./01-problem-hypothesis-v0.1.md)
> **方法论**：Playbook Idea Stage — Competitor mapping + tier-based threat analysis

---

## 0. TL;DR（一图三句）

```
            国内 Agent 工具链生态地图（2026-05）

   设计端       开发端          部署端           运维/观测端
  ─────────    ─────────       ─────────         ─────────
  Dify       │ AgentScope    │ AgentScope     │ ARMS / Cloud Trace
  Coze       │ LangGraph     │ Runtime        │ AgentScope
  FastGPT    │ 通义灵码 IDE  │ 百炼/PAI/FC    │   Studio
  ──────────┼──────────────┼──────────────┼─────────
   ⚠ 我们的目标定位 = 用统一 CLI/Skills 跨整条链路, 让 coding agent 一次接管
```

1. **直接竞品**：Google `agents-cli`（海外样板）。
2. **最致命邻接玩家**：阿里 AgentScope Runtime + 百炼 ModelStudio + 通义灵码 `create-agent` —— 已覆盖中后半段。
3. **三根定位支柱**（待验证）：(A) 面向**对外发布的商业级 Agent**而非 IDE 内部 agent；(B) 覆盖**Idea→Design** 前半段；(C) 为**任意 Coding Agent** 设计的 Skills 抽象。

---

## 1. 玩家全景（按"对我们的杀伤距离"排序）

| 玩家 | 类型 | 在我们四段链路里的位置 | 杀伤距离 |
|---|---|---|---|
| Google `agents-cli` | 直接竞品（海外） | 全段 | ⭐⭐⭐⭐ |
| 阿里 AgentScope Runtime | 邻接（同生态） | 开发-部署-运维 | ⭐⭐⭐⭐⭐ |
| 阿里云百炼 ModelStudio | 邻接（同生态） | 开发-部署 | ⭐⭐⭐⭐ |
| 通义灵码 (Qoder CN) `create-agent` | 邻接（分发渠道） | 开发（IDE 内） | ⭐⭐⭐⭐ |
| 阿里云 PAI LangStudio CLI | 邻接（API 层） | 部署 | ⭐⭐⭐ |
| Dify / Coze / FastGPT | 间接（低代码平台） | 设计-开发（部分） | ⭐⭐ |
| LangChain/LangGraph CLI | 间接（开源框架） | 开发 | ⭐⭐ |

---

## 2. 五个关键玩家详拆（每条都给"赢/输"对照）

### 2.1 ⭐⭐⭐⭐ Google `agents-cli`（直接竞品 + 我们的灵感来源）

- **核心命题**：让任意 Coding Assistant（Gemini CLI / Claude Code / Codex / Antigravity）成为 GCP Agent 平台的专家。
- **架构**：CLI 命令 + 7 个 Skills（workflow / adk-code / scaffold / eval / deploy / publish / observability）。
- **实际状态**：GitHub ~2.5k stars，~20 commits，Issues ~9，2026 年初发布——**说明 Google 自己也是新业务，国内可借鉴的"现成答卷"非常成熟**。
- **他们为什么会赢**：背靠 Gemini Enterprise Agent Platform；Skills 模式非常贴合"教会 coding agent 调云"的范式。
- **他们为什么搬不到中国**：GCP 在国内份额近 0；Gemini API 国内不可用——**这恰恰是我们的机会窗**。

### 2.2 ⭐⭐⭐⭐⭐ 阿里 AgentScope Runtime（最致命邻接，必须正面回应）

- **核心命题**：阿里巴巴自家的 Agent 框架 + 运行时；支持一键部署到 ACS / 百炼 / FastAPI。Java v1.0 已发布。
- **覆盖范围**：**开发框架 + 部署 + Runtime 安全沙箱**。
- **不覆盖**：Idea/Design 前半段；针对 coding agent 调用的 Skills 抽象层。
- **他们为什么会赢**：阿里官方品牌、和百炼生态深度绑定、企业可信。
- **我们必须证明的**：在 AgentScope Runtime 之上加一个"面向 coding agent 的 Skills 包 + 设计端工作流"，对开发者是有增量价值的，**而不是重复造轮子**。
- ⚠ **致命风险**：如果阿里官方在未来 6 个月给 AgentScope 加 Skills 层（极有可能），我们这层立刻失去差异化。
- 🛡 **缓释路径**：定位成"AgentScope 的社区 cookbook 增强 + 跨 Coding Agent 适配层"，不和官方正面冲突，做官方不愿做的"长尾适配"。

### 2.3 ⭐⭐⭐⭐ 阿里云百炼 ModelStudio

- **核心命题**：企业级大模型应用开发平台；零代码 Agent + 高代码 API（基于 AgentScope-AI）。
- **覆盖范围**：开发-部署-应用发布。
- **关键事实**：百炼**已写完高代码应用 API 开发指南**，明确推荐 AgentScope-AI 作为开发框架——这等于阿里官方钦定了 Agent 开发栈。
- **他们的 gap**：控制台为主，CLI/SDK 体验对 Coding Agent 不友好；缺设计端模板。

### 2.4 ⭐⭐⭐⭐ 通义灵码 `create-agent`（最危险的分发渠道竞争）

- **核心命题**：阿里云官方 IDE 助手；Qoder CN 智能体模式；提供 `create-agent` 用于自定义 IDE 内 agent。
- **关键区分（Pillar A）**：灵码 `create-agent` 创建的是**IDE 内部、给开发者本人用**的 agent；我们要做的是**对外发布、给最终用户用**的商业级 agent。**这个区分是我们差异化的命脉。**
- **他们为什么会赢**：默认装机量、和 IDE 深度集成、阿里云原生支持。
- ⚠ **致命风险**：灵码哪天把 `create-agent` 的目标对象从"IDE 内"扩展到"对外应用"，我们就失去 Pillar A。
- 🛡 **缓释路径**：刻意保持"独立于任何 IDE/Coding Agent"——能在 Claude Code / Cursor / Codex / Qoder / 灵码 / Gemini CLI 任意一个里跑——这个**跨工具兼容性**正是 google/agents-cli 走通的路子。

### 2.5 ⭐⭐⭐ 阿里云 PAI LangStudio CLI

- **核心命题**：阿里云 OpenAPI 门户提供的 PAI 大模型应用开发 CLI；能调 `CreateDeployment` 等 API。
- **gap**：典型的"OpenAPI 包一层"工具，没有"workflow/eval/observability"的高阶 Skills，体验偏底层。
- **对我们的启示**：可以**直接复用 PAI/百炼的底层 OpenAPI**，我们专注做上层 Skills 与跨 coding agent 的适配——节省工作量。

### 2.6 ⭐⭐ Dify / Coze / FastGPT（间接竞品 / 不构成正面威胁）

- **定位差异**：他们是**低代码 Agent 平台**，目标用户是"不写代码的产品经理 / 业务方"。我们的目标用户是"在阿里云上写代码做 Agent 的工程师"。**正面冲突很弱**。
- **可以利用的**：他们的爆发证明了"Agent 开发需求"客观存在；他们的"完美图形界面" vs 我们的"CLI + Skills" 是清晰的产品形态分野。

### 2.7 ⭐⭐ LangChain / LangGraph CLI（国际开源生态）

- **不构成威胁**：是开发框架而非云上 CLI；与我们正交。
- **可被吸纳**：我们的 Skills 可以同时支持 LangGraph / AgentScope 两套写法，扩大生态。

---

## 3. 三根定位支柱 → 翻译成"我们做的 / 不做的"

| 支柱 | 我们做 | 我们不做 |
|---|---|---|
| **A. 商业级对外 Agent** | 一键脚手架包含：API 网关、用户 session、配额、计费埋点、合规日志 | IDE 内部辅助 agent（让灵码做） |
| **B. 全生命周期含 Idea/Design** | 提供 problem-hypothesis、user-discovery、scope-doc、CLAUDE.md 模板等"前半段 Skills" | 重新发明 Agent 框架（直接复用 AgentScope/LangGraph） |
| **C. 跨 Coding Agent 友好** | 输出符合 Anthropic Skills / Gemini Skills / OpenAI Codex Skills 三套规范的同一份知识包 | 绑定单一 IDE / 单一 coding agent |

---

## 4. Step 3 必须用证据验证的 5 件事

> 不做正式访谈，但必须有公开证据/原话/同事观察来源。

1. **Pillar A 证据**：找 ≥3 条公开原话或自身观察，证明"工程师确实需要把 Agent 对外发布给终端用户用"——而不是只在 IDE 内自用。
2. **Pillar B 证据**：找 ≥3 条原话或观察，证明工程师在"Idea → Design"前半段确实有痛、确实希望工具替他规整。
3. **Pillar C 证据**：找 ≥3 条原话或观察，证明工程师在用多个 coding agent（不是只用一个），且为它们做适配是真痛。
4. **R1 持续监控**：建立一份"阿里云官方动作 watchlist"，每两周扫一次百炼 release notes / AgentScope release notes / 灵码更新日志，看是否出现侵入我们 niche 的动作。
5. **R8 自检**：列 8 位你认为"和你一样痛"的真人，在心里完成一次"如果我去问他，他会同意我哪几条？"的预演。

---

## 5. 给 demo 项目的现实切片

> 因为是 GitHub Star 项目 / demo 性质，不必做完所有 7 个 Skill。

**MVP 切片建议（待 Step 4 决策时拍板）**：先做 **3 个 Skill**——
- `bailian-scaffold`：基于一句话需求，生成结构化 Agent 项目骨架（含 README、`.lingma`/`.claude`/`.cursor` 三套上下文文件）。
- `bailian-deploy`：一键把生成的 Agent 部署到百炼 / 函数计算 / SAE。
- `bailian-eval`：跑 Anthropic 风格的 evalset + LLM-as-judge。

剩下 4 个（observability、publish、workflow、adk-code）放 Roadmap，**用"延迟满足"逼自己保持纪律**——不让 Qoder 在 MVP 阶段无序扩张。

---

*本文件随 Step 3 证据收集结果迭代到 v0.2。*
