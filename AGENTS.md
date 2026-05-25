# AGENTS.md — agent-cli-alicloud

`agent-cli-alicloud` 让任意 Coding Agent 把一句模糊的 Agent 想法，5 分钟内变成结构化设计文档（AGENTS.md / scope.md / eval-plan.md）+ 可被 AgentScope/AgentRun/百炼直接消费的脚手架。

> **Source of Truth**：本文件与代码冲突时本文件赢；与商业判断冲突时先更新本文件再让代码跟进。
> 教学注解版见 `founder-playbook/AGENTS-annotated.md`（不参与每次会话加载）。

---

## IMPORTANT — Three Positioning Pillars（任何 PR 不许偏离）

- **A.** 商业级**对外发布**的 Agent，不是 IDE 内部 Agent
- **B.** 覆盖 **Idea / Design 前半段**，不重做 Runtime / 框架 / 部署
- **C.** **跨 Coding Agent 友好**——任意 Coding Agent 都能消费产物

## IMPORTANT — What we DO NOT do

- ❌ 重做 Agent 框架（生成 AgentScope / LangGraph 兼容代码即可）
- ❌ 重做 Runtime / Sandbox（复用 AgentRun / FC / SAE）
- ❌ 重做 **runtime 图形化 workflow 编排器**（百炼工作流应用 / Dify / n8n）
- ❌ 绑定单一 Coding Agent / 单一 IDE

## IMPORTANT — Workflow disambiguation

本项目 `workflow` **永远指 dev-time 方法论 Skill**（同 Google `agents-cli` 的 `workflow` skill 概念）：被 coding agent 读取后引导开发者走"想法→澄清→设计→脚手架"。
**百炼 workflow application / Dify / n8n** 是 **runtime 节点编排器**——不是竞品也不是覆盖。
PR / 文档 / 代码注释**禁止混用**这两个词，必要时用 `dev-workflow` / `runtime-workflow` 区分。

---

## YOU MUST — Coding Agent Session Protocol

### Pre-flight（每次 session 开始）
1. 读完本文件
2. 读 `@founder-playbook/mvp/scope.md` 末尾 §3 Feature Amendment 门槛
3. 读 `@founder-playbook/mvp/SESSION-LOG.md` 末尾 3 条

### In-session
- **不新增依赖**，除非 PR 描述写清"为什么 stdlib + 已有依赖搞不定"
- **不重命名公共 API**（`agent_cli_alicloud.*`）符号
- **不扩 scope**——冲动时把它写进 `founder-playbook/mvp/SCOPE-PROPOSALS.md` 等创始人审批

### Post-flight（每次 session 结束）
1. 在 `@founder-playbook/mvp/SESSION-LOG.md` 追加一条记录（格式见该文件顶部）
2. 若本次让本文件失真，**必须先更新本文件再 commit 代码**
3. 跑下面 Verify，失败禁止结束

---

## Verify

```bash
uv run pytest
uv run ruff check
uv run mypy src/agent_cli_alicloud/core
```

`make verify` 是上述三条的集合命令。修改 `templates/` 后 golden 测试若失败，**先评估"是模板有问题还是 golden 过期"**，不要无脑刷新 golden。

---

## Tech Stack（已拍板，PR 不要换）

| 层 | 选型 |
|---|---|
| 语言 | Python 3.11+ |
| 项目管理 | **uv**（不用 pip / poetry / pdm） |
| CLI 框架 | **typer**（不用 click / argparse） |
| 模板引擎 | **jinja2** |
| ~~LLM 调用~~ | **CLI 层永不调 LLM**（v0.2 铁律）。LLM 调用由用户 Coding Agent + Skill 层引导完成，CLI 不参与 |
| 测试 | pytest + pytest-asyncio |
| Lint / Format | ruff |
| 类型 | mypy strict（仅 `core/` 模块） |
| 分发 | PyPI（`uvx agent-cli-alicloud`）+ GitHub repo（`./install.sh`） |

代码 anchor：`src/agent_cli_alicloud/` 下分 `cli.py` / `core/` / `skills/` / `templates/`；详细见 `@founder-playbook/mvp/01-mvp-spec.md`。

---

## Project-specific Rules

- **用户可见文案统一中文**（产品定位国内市场）
- **CLI 层禁止依赖任何 LLM SDK / 网络 IO**——若某段逻辑必须涉及 LLM，必须先在 `scope.md` §2 论证为何不能放 Skill 层
- **错误信息格式**：`raise ValueError(f"…，建议：…")`（建议项可被 Coding Agent 直接读懂）
- **golden snapshot 测试**：`init` 命令必须有，路径 `tests/golden/xiaohongshu_demo/`，且**不依赖 LLM / 不依赖网络 / 不需要 API key**
- **Skill 改写来源**：Google `agents-cli/skills/` 目录下对应 SKILL.md 为骨架，按 4 步本地化（见 `01-mvp-spec.md` §3.1）

## YOU MUST — Security

- CLI 不读取 `DASHSCOPE_API_KEY`（它不调 LLM）；若 Skill 引导 Coding Agent 生成的代码需要 key，该代码自行从 `.env` 或环境变量读取
- 用户输入**默认不上传任何第三方** telemetry
- 公开发布前跑 `bandit -r src/`，零高危才能 release
- **红线机械化检查**：`grep -r "dashscope\|openai\|httpx\|requests" src/agent_cli_alicloud/` 不得有业务代码命中

---

## Imports

- `@founder-playbook/mvp/scope.md` — In/Out + Feature Amendment 硬门槛（v0.2 双层架构）
- `@founder-playbook/mvp/01-mvp-spec.md` — CLI + Skills 验收规格（v0.2，含 golden snapshot + Skill 改写策略）
- `@founder-playbook/mvp/SESSION-LOG.md` — Coding Agent 历史记录
- `@founder-playbook/r1-watchlist.md` — 竞品监控（创始人每两周 review，coding agent 不需关心）
