# AGENTS-annotated.md — 教学注解版

> **本文件不是 Coding Agent 的工作输入**——根目录精简版 [`AGENTS.md`](../AGENTS.md) 才是。
> 本文件保留了优化前的"重量级"版本，并对每一节标注：**对照 Anthropic [Effective CLAUDE.md 最佳实践](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md) 之后，该节为什么被精简 / 移除 / 拆走**。
> 用途：让创始人在以后写其他项目的 AGENTS.md / CLAUDE.md 时有教材可对照。

---

## Anthropic 最佳实践浓缩（5 条）

1. 每行问"删掉它 Claude 会出错吗？"——不会就**删**
2. 文件太长会让 Claude 忽略真正重要的规则——**这是头号失效模式**
3. 不要写"Claude 看代码就能推断的东西"（语言默认规范、文件结构、API 文档、自明实践）
4. 频繁变化的信息（stage、roadmap 进度）**不要进**——会过期变垃圾
5. 用 `@path/to/file` 把"偶尔需要"的内容拆出去；**关键纪律加 `IMPORTANT` / `YOU MUST` 强调**

加分项：提供 verify 命令（"highest-leverage thing"）；标准例子是 ~10 行不是 140 行。

---

## 优化前原文 + 每节注解

> 下文每节末尾的 🟢 / 🟡 / 🔴 注解记录了精简决策。

### § 头部（"任何 Coding Agent 必须先读完本文件…"）

> 本文件是项目级架构上下文文档。任何 Coding Agent 在开始任何编码任务前都必须先读完本文件。
> 创始人在每次 Coding Session 开始与结束时也必须复读 / 更新本文件。
> 本文件同时是其它 Coding Agent 上下文文件的唯一信源——其它文件全部由本文件派生。

🟡 **保留要点，但精简一半**——Coding Agent 默认就读 AGENTS.md，不需要长篇大论强调。精简版只保留 "Source of truth" 一句话。

---

### § 1. Project Identity

#### 1.1 Name / One-liner / Pillars / What we don't do

🟢 **必留**：Pillars 和 What we don't do 是项目特有 architectural decisions，正是 Anthropic 表格里"✅ Architectural decisions specific to your project"那一项。
精简版给三条 Pillars 和拒绝清单加了 `IMPORTANT` 标记。

#### 1.2 **Stage**：Idea Stage 已结束 → 正在进入 MVP Stage

🔴 **删除**——典中典的"频繁变化的信息"（Anthropic 警告：Information that changes frequently 不要进）。
Stage 应该放在 SESSION-LOG.md 顶部，每次 session 结束时更新。

#### 1.3 What we DO mean by "workflow"（dev-time vs runtime 区分）

🟢 **必留**——这是非显然的项目专属 gotcha，对应 Anthropic"✅ Common gotchas or non-obvious behaviors"。
精简版保留并加 `IMPORTANT` 标签。

---

### § 2. MVP Single Core Interaction（30+ 行 ASCII 命令演示）

🟡 **从 30 行压成 2 行 + `@import`**——核心思想必留（"只围绕一个核心交互"）但完整 demo 命令属于 mvp-spec.md，应该用 `@import` 引用而不是重复。
Anthropic 原话："use `@path/to/import` syntax to import additional files"。

---

### § 3. Tech Stack（uv / typer / jinja2 表格）

🟢 **必留**——所有选项都是**非默认**选择，正是 Anthropic"Bash commands Claude can't guess + 项目特有架构决策"的范本。
精简版保留表格，但 lint / mypy 等列只留必要项。

---

### § 4. Repository Layout（完整 ASCII 树）

🔴 **删除**——Anthropic 表格明列"❌ File-by-file descriptions of the codebase"应该排除。Coding Agent `ls` 一下、读一下 pyproject.toml 全都能推断。
精简版只保留 1 句话提示"src/agent_cli_alicloud/ 下分 cli/core/skills/templates"作为 anchor，剩下让 agent 自己探索。

---

### § 5. Coding Agent Session Protocol（Pre / In / Post-flight）

🟢 **核心保留**——这是项目最重要的 workflow 纪律，对应 Anthropic"✅ Repository etiquette"。
精简版调到顶部靠前位置（仅次于 Pillars），并加 `YOU MUST` 强调。
Anthropic 原话："tune instructions by adding emphasis (e.g., IMPORTANT or YOU MUST) to improve adherence"。

---

### § 6. Naming & Style Conventions（snake_case / PascalCase 等）

🔴 **大半删除**——Python PEP 8 默认就是这些，Anthropic 表格明确"❌ Standard language conventions Claude already knows"。
**仅保留**两条非默认项：
- 用户可见文案统一中文（产品定位特殊）
- LLM Prompt 集中在 `core/llm.py`（项目特殊架构决策）

---

### § 7. Testing Convention

🟡 **部分留**——"每个模块对应 test_*.py"是 pytest 默认实践应删；
**保留**："golden snapshot 测试 + 修改 templates 时不要无脑刷新 golden"——这是项目特殊纪律，Anthropic"non-obvious behaviors"。

---

### § 8. Security & Compliance

🟢 **保留**——API key 不落盘、不打日志、telemetry 默认关闭，全是项目特有约束。
精简版加 `YOU MUST` 强调。

---

### § 9. R1 Watchlist（每两周创始人 review）

🔴 **拆出去**——这不是 Coding Agent 每次 session 都需要的，是创始人决策面板。
拆到独立文件 `founder-playbook/r1-watchlist.md`，AGENTS.md 里只放 1 行 `@import` 链接。
Anthropic 原话："CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead."

---

### § 10. Source of Truth Rule

🟢 **保留**——项目宪法，简短，必须每次加载。

---

### 缺失项（精简版新增）

#### Verify commands

🆕 **必须新增**——Anthropic 原话："Include tests, screenshots, or expected outputs so Claude can check itself. **This is the single highest-leverage thing you can do.**"
精简版新增 `## Verify` 节，给出 `uv run pytest && uv run ruff check && uv run mypy src/agent_cli_alicloud/core` 的明确命令。

#### `@import` 引用

🆕 **必须新增**——把 mvp/scope.md, mvp/01-mvp-spec.md, mvp/SESSION-LOG.md, r1-watchlist.md 用 `@` 显式引用，让 Coding Agent 知道何时去查更详细的上下文。

---

## 最后的预算账

| 项 | 原文 | 精简版 |
|---|---|---|
| 行数 | ~140 行 | ~70 行 |
| 章节数 | 10 节 | 6 节（合并 Naming/Testing 进 "Project rules"） |
| 频繁变化的信息 | 1 处（Stage） | 0 |
| Python 默认规范 | 5 行 | 0 |
| Repo Layout 完整树 | 30 行 | 1 行 anchor |
| `YOU MUST` 强调 | 0 处 | 4 处（关键纪律） |
| `@import` 链接 | 0 | 4 处 |
| Verify 命令 | 0 | 1 节 |

---

## 这次教学的可迁移结论

1. **AGENTS.md / CLAUDE.md 不是项目说明书**——它是一份"每次会话都要重新念一遍"的 cheatsheet，所以"每次都念一遍代价是否值得"是它的唯一编辑标准。
2. **频繁变化的信息（stage、版本号、roadmap 进度）一定不能进**——它们的归属是 SESSION-LOG / CHANGELOG / Issue tracker。
3. **不要把"读着好看的文档"和"对 LLM 高效的 context"搞混**——前者重叙述、有铺垫；后者重密度、要有 verify 命令、要用强调标签。
4. **拆与合**：把"偶尔需要"的拆到 `@import`；把"完整说明"留给 `*-annotated.md` / `README.md`；把"标准实践"交给语言/工具默认值，不要写进 AGENTS.md。
5. **Anthropic 这页指南本身就是 dogfooding**：它的列表对照表、do/don't 表格、关键警告（"too long → ignored"）正是 high-density 写作的范本。

*完。*
