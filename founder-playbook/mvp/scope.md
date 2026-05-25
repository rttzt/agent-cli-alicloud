# MVP Scope Doc v0.2

> Playbook 第 17 页：**"a written scope definition created before building begins, describing what the product does, what it deliberately does not do, and the specific evidence from real users that would justify adding something new."**
>
> 任何"顺手把 X 加进来"的冲动，请先回到本文件论证。
> 任何 Coding Agent 接到 PR 任务，本文件优先级仅次于 AGENTS.md。

> **v0.2 重大调整（2026-05-22）**：范式从"Python CLI + LLM 业务逻辑"切换为 **CLI + Skills 双层架构**，对齐 Google `agents-cli` 的 Skill = Cognitive Layer / CLI = Action Layer 模式。
>
> 核心认知：**Skill 解决"知道怎么做"，CLI 解决"稳定地做成"**。澄清问答 + 设计文档生成属于认知工作，搬到 Skill 由用户的 Coding Agent 执行；项目脚手架 + 状态管理 + 升级合并属于执行工作，由 CLI 确定性完成。

---

## 1. MVP 做什么（IN SCOPE）

### 1.1 CLI 层（确定性执行，Python 实现，**不调任何 LLM**）

| # | 命令 | 验收标准 |
|---|---|---|
| C1 | `agent-cli setup` | 检测本机已装的 Coding Agent（Qoder / 通义灵码 / Claude Code / Cursor），把 4 个 Skill 复制到对应 skills 目录；输出"已装到 X 个 agent" |
| C2 | `agent-cli init <name> [--template agentscope]` | 纯 jinja2 模板渲染，生成 AgentScope 兼容项目骨架 + `agent-cli-manifest.yaml`；不调 LLM、不问问题、可重复执行；接收的是项目名（不是 idea 一句话） |
| C3 | `agent-cli info` | 读 manifest，输出项目名 / 模板 / agent 目录 / CLI 版本，支持 JSON 与人类可读两种模式 |
| C4 | `agent-cli-manifest.yaml` 状态文件 | 由 `init` 创建，记录 `name / template / agent_directory / cli_version / created_at`，是未来 `scaffold upgrade` 命令做 3-way merge 的基础 |
| C5 | 双轨分发：PyPI + GitHub repo + `install.sh` | `uvx agent-cli-alicloud setup` 与 `git clone + ./install.sh` 都能跑 |
| C6 | golden snapshot 测试覆盖 init 命令 | `pytest -k golden` 通过；测试不依赖 LLM、不依赖网络 |

### 1.2 Skill 层（认知引导，Markdown 实现，由用户的 Coding Agent 消费）

| # | Skill | 内容范围 |
|---|---|---|
| S1 | `agent-cli-alicloud-workflow/SKILL.md` | dev-time 方法论：从一句 idea 到设计文档的完整引导（5 个澄清问题、AGENTS.md 写作要点、scope.md 模板、eval-plan.md 思路、何时调 `agent-cli init`、何时切到下一个 Skill）— **核心差异化（Pillar B）** |
| S2 | `agent-cli-alicloud-scaffold/SKILL.md` | 何时调 `agent-cli init`、模板选择、目录约定、与 AgentScope 的对接点 |
| S3 | `agent-cli-alicloud-deploy/SKILL.md` | 部署目标决策（百炼应用 / 函数计算 AgentRun / SAE）、何时使用 AgentScope `deploy()` 一键打包；**MVP 阶段为决策树占位**，实际部署逻辑 Roadmap |
| S4 | `agent-cli-alicloud-eval/SKILL.md` | 评测集 schema、5 维度评分（召回 / 拆解 / 可行性 / 合规 / 时延）；**MVP 阶段为评测方法论占位**，实际 eval harness Roadmap |

### 1.3 Demo 验收场景：小红书爆文分析 Agent

| # | 验收路径 | 验收标准 |
|---|---|---|
| D1 | 用户跑 `agent-cli setup` → 在 Qoder 中说"我想做一个能帮品牌方分析小红书爆文的 Agent，请用 agent-cli-alicloud" | Qoder 自动加载 workflow Skill，按 SKILL.md 引导走 5 个澄清问题 |
| D2 | Qoder 引导用户产出 AGENTS.md / scope.md / eval-plan.md | 三份文档由 Qoder 生成，**不由 CLI 生成**（CLI 不调 LLM） |
| D3 | Qoder 调 `agent-cli init xiaohongshu-trend-agent --template agentscope` | 生成确定性项目骨架 + manifest |
| D4 | golden snapshot 覆盖 `agent-cli init` 输出 | 模板渲染结果稳定可比对，不依赖 LLM |

---

## 2. MVP 不做什么（OUT OF SCOPE — Roadmap 候选）

| 能力 | 为什么现在不做 | 进 MVP 的触发条件 |
|---|---|---|
| **CLI 内调 LLM 生成澄清/文档**（v0.1 IN SCOPE 项 #2/#3） | 范式根本转向：认知工作交给用户的 Coding Agent + workflow Skill，CLI 保持纯执行层 | **永久 OUT**——除非确认 Coding Agent 引导效果普遍不达标 |
| `agent-cli scaffold upgrade`（3-way merge 项目升级） | 需要 manifest 沉淀 + 真实用户老项目才有意义；MVP 阶段 manifest 已埋点 | ≥3 个老项目用户报"想升级到新模板" |
| `agent-cli deploy` 真实部署到百炼 / FC / AgentRun | AgentRun / AgentScope `deploy()` 已极致便捷；MVP 阶段 deploy Skill 提供决策树即可 | 用户原话明确说"我希望你也包了部署" |
| `agent-cli eval run` 真实跑评测 | 商业级 Eval 是空白，但比设计端工作量高 5 倍 | demo PMF 达成（≥10 star + 3 反馈）后再启动 |
| `agent-cli run "prompt"`（本地 echo agent） | Google 有，但 AgentScope 自带 playground，不重复造 | 用户反馈"不想切换工具" |
| 跨多 Coding Agent 适配文件（CLAUDE.md / .cursorrules / 灵码 .lingmarules） | Skills 已经是 markdown 通用格式；各 Coding Agent 自身入口约定走 `setup` 命令分发解决 | ≥3 位真实试用者反馈"我用的 X 没装上" |
| 图形化 **runtime workflow 编排器**（百炼工作流应用 / Dify / n8n） | runtime 层不是我们的层，本项目 `workflow` 是 dev-time 方法论 Skill | 永久 OUT |
| Web UI / Dashboard | CLI + Skill 才是 Pillar C 的载体 | 永久 OUT |
| 多语言（英文 README 之外的本地化） | 国内市场为主 | Star ≥100 时再说 |
| **CLI 依赖任何 LLM SDK / 网络 IO** | DashScope 调用已搬到 Skill 引导用户的 Coding Agent；CLI 应该可在离线、无 API key 环境下完整运行 | 永久 OUT for CLI |

---

## 3. Feature Amendment Criteria（新功能进 MVP 的硬门槛）

> 任何创始人 / 贡献者 / Coding Agent 想加新功能进 MVP，必须**全部**满足下列条件：

1. **真实用户原话**：≥3 位试用者用自己的话说出"没有 X 我没法用这个工具"——**不是"我希望有 X"**
2. **Pillar 一致性**：必须明确属于 Pillar A / B / C 之一，并写出对应映射
3. **拒绝清单复检**：不在 AGENTS.md §1 拒绝清单里
4. **可验收的小 PR**：能在一个 Coding Agent session 里完成；超过的拆分
5. **Devil's Advocate 自问**：写一段反驳"为什么这个功能其实不该做"，并回应
6. **【v0.2 新增】层归属判断**：明确说出该功能属于 **CLI 执行层** 还是 **Skill 认知层**——
   - 若需要 LLM 推理 / 判断 / 生成 → 属于 Skill 层，写进 SKILL.md，不进 CLI 代码
   - 若是确定性文件操作 / 模板渲染 / 状态管理 → 属于 CLI 层
   - 若两者都需要 → 拆成两个 PR，先做 Skill 再做 CLI（CLI 提供 Skill 调用的稳定动作）

---

## 4. False Positive 定义（哪些信号不算 PMF）

> Playbook 第 19 页提醒：建立"什么不算 PMF"的定义，比建立"什么算 PMF"更重要。

不算的：
- 你自己用得很爽（你是 ICP，自证不算证）
- GitHub Star 但没人提 issue / 没人发反馈（Star 是好奇，不是用过）
- 朋友圈点赞 / 转发量
- 微信群里别人说"看起来挺好"
- LLM 评审说生成的 AGENTS.md "质量很高"

算的：
- ≥3 位试用者**用 init 跑过自己的 idea**，且其中 ≥1 位写出 ≥100 字的具体反馈（哪好哪不好）
- ≥1 个非创始人发 PR
- ≥1 个 issue 标 `bug` 标签——意味着有人真的用到崩了
- 有人在公开渠道（小红书/知乎/掘金/V2EX）写一篇引用本工具的文章

---

## 5. Demo Scenario Spec：小红书爆文分析 Agent

> 这是我们走通 MVP 单一核心交互的"打靶用例"，golden snapshot 测试以它为基准。

**用户输入（一句话）**：
> 我想做一个能帮品牌方分析小红书爆文的 Agent

**期望产出（在用户当前目录下）**：

```
xiaohongshu-trend-agent/
├── AGENTS.md             # 场景化的项目说明
├── scope.md              # 列出此场景的 in/out
├── eval-plan.md          # 给出 5 条评测样例 + 评分维度
├── clarification.md      # 5 个澄清问题与默认答案
├── next-steps.md         # 建议接给 Coding Agent 的 3 个任务
├── pyproject.toml
└── src/agent/
    ├── __init__.py
    ├── main.py           # AgentScope 兼容的最小可跑骨架
    └── tools/
        └── xhs_search.py # 占位：调小红书检索的伪实现
```

**5 个澄清问题（固定）**：
1. **谁是终端用户？**（默认：品牌方运营/内容策划）
2. **触发方式？**（默认：用户提供品类关键词或竞品账号）
3. **输入数据来源？**（默认：小红书搜索 API / 第三方爬虫，需用户配置）
4. **输出形态？**（默认：结构化的爆文要素拆解 + 选题建议）
5. **合规与隐私？**（默认：仅分析公开内容，不存储个人 ID）

---

## 6. SESSION-LOG 起始（占位）

```
=== SESSION-LOG ===
（每次 Coding Agent session 结束时由该 agent 自己 append）
```

---

*更新策略：每个 MVP-x 阶段结束时 bump 到 v0.2 / v0.3 …*
