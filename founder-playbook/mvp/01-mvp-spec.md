# MVP-2 Spec v0.2 — CLI + Skills 双层架构

> **本文件是给 Qoder Quest 专家组的工作单。** Quest 必须按本规格交付。
> 本文件优先级：AGENTS.md > scope.md > **本文件** > 其它。
>
> **v0.2 重大调整（2026-05-22）**：范式从"Python CLI + LLM 业务逻辑"切换为 **CLI + Skills 双层架构**，对齐 Google `agents-cli`。
> 详见 `scope.md` v0.2 §1（IN SCOPE 二分：CLI 层 / Skill 层 / Demo 路径）。
>
> **核心铁律**：CLI 层**永远不调 LLM、永远不发网络请求**（除分发本身）。所有认知工作搬到 Skill 层，由用户的 Coding Agent 消费。

---

## 1. Quest 在 MVP-2 的唯一目标

交付一个 **CLI + 4 个 Skill** 组成的最小可用产品，使下面三方协作流程能 demo 跑通：

```
用户                Coding Agent (Qoder/灵码)              agent-cli (本项目)
 │                        │                                      │
 ├──$ agent-cli setup ───────────────────────────────────────────▶│
 │                        │◀───────  Skills 装入 IDE  ────────────┤
 │                        │                                      │
 ├──"我想做小红书爆文 Agent" ─▶│                                      │
 │                        ├─读 workflow Skill                    │
 │                        ├─走 5 个澄清问题（Skill 引导）          │
 │                        ├─生成 AGENTS.md / scope.md / eval-plan.md
 │                        │                                      │
 │                        ├──$ agent-cli init xiaohongshu... ───▶│
 │                        │◀── 项目骨架 + manifest.yaml ──────────┤
 │                        │                                      │
 │                        ├─继续填 src/agent/main.py（参考 scaffold Skill）
 ▼                        ▼                                      ▼
```

**不要**在 MVP-2 实现：
- `agent-cli scaffold upgrade`（3-way merge，Roadmap）
- `agent-cli deploy / eval / publish` 真实执行（仅 Skill 占位）
- 任何 LLM 调用 / 网络 IO / DashScope SDK 依赖
- Web UI / telemetry / 多语言

---

## 2. CLI 层命令规格

### 2.1 `agent-cli setup`

**职责**：把本仓库 `skills/` 目录下的 4 个 SKILL.md 复制到本机已安装的 Coding Agent 各自的 skills 目录。

**输入**：无参数（可选 `--target qoder|lingma|claude-code|cursor` 指定单个目标，默认 all-detected）。

**检测逻辑**（按存在性检测，不存在则跳过）：

| Coding Agent | 检测路径（macOS） | 安装目标路径 |
|---|---|---|
| Qoder | `~/.qoder/skills/` | `~/.qoder/skills/agent-cli-alicloud-{name}/SKILL.md` |
| 通义灵码 | `~/.lingma/skills/` 或 IDE 插件目录占位 | `~/.lingma/skills/agent-cli-alicloud-{name}/SKILL.md` |
| Claude Code | `~/.claude/skills/` | `~/.claude/skills/agent-cli-alicloud-{name}/SKILL.md` |
| Cursor | `~/.cursor/rules/` | `~/.cursor/rules/agent-cli-alicloud-{name}.md`（rule 形式） |

**Windows / Linux 路径**：与 macOS 同结构，仅 `~` 用 `pathlib.Path.home()` 解析。

**输出**：
```
$ agent-cli setup
✓ Detected: Qoder (~/.qoder/skills/)
✓ Detected: 通义灵码 (~/.lingma/skills/)
✗ Skipped: Claude Code (not installed)
✗ Skipped: Cursor (not installed)

Installed 4 skills to 2 coding agents:
  - agent-cli-alicloud-workflow
  - agent-cli-alicloud-scaffold
  - agent-cli-alicloud-deploy
  - agent-cli-alicloud-eval

Next: open your coding agent and tell it your idea, e.g.
  "我想做一个小红书爆文分析 Agent，请用 agent-cli-alicloud"
```

**幂等性**：重复跑 `setup` 不报错，同名 SKILL.md 直接覆盖。

**禁止**：调任何网络、写任何 home 之外的路径、修改用户已有 SKILL.md 之外的文件。

---

### 2.2 `agent-cli init <name> [--template agentscope]`

**职责**：纯 jinja2 模板渲染，生成 AgentScope 兼容项目骨架 + `agent-cli-manifest.yaml`。

**输入**：
- 必填：`<name>`（项目名，将作为目录名，必须符合 `^[a-z][a-z0-9-]{1,63}$`）
- 可选：`--template`（默认 `agentscope`，MVP-2 仅此一个；Roadmap 添加 `langgraph` / `bailian-app`）
- 可选：`--dir`（输出目录，默认当前目录）
- 可选：`--force`（覆盖已存在目录）

**示例**：
```
$ agent-cli init xiaohongshu-trend-agent
✓ Created xiaohongshu-trend-agent/ (template: agentscope)
  ├── pyproject.toml
  ├── src/agent/__init__.py
  ├── src/agent/main.py
  ├── src/agent/tools/__init__.py
  ├── src/agent/tools/placeholder.py
  ├── tests/test_main.py
  ├── .env.example
  ├── README.md
  └── agent-cli-manifest.yaml

Next: open this directory in your coding agent and let it fill in the design docs.
```

**禁止**：
- 调 LLM、读环境变量 `DASHSCOPE_API_KEY`、走任何网络
- 询问用户任何问题（澄清问题归 workflow Skill 管）
- 生成 `AGENTS.md` / `scope.md` / `eval-plan.md`（这三份是 Coding Agent 在 Skill 引导下产出的，不是 CLI 产出的）

---

### 2.3 `agent-cli info`

**职责**：读当前目录的 `agent-cli-manifest.yaml`，输出项目状态。

**输入**：可选 `--format json|text`（默认 text）。

**输出（text 模式）**：
```
$ agent-cli info
Project: xiaohongshu-trend-agent
Template: agentscope (v0.1.0)
Agent directory: src/agent
CLI version: 0.2.0 (created 2026-05-22)
Manifest: ./agent-cli-manifest.yaml
```

**输出（json 模式）**：直接 dump manifest 内容 + 当前 CLI 版本，给 Coding Agent 解析用。

**错误处理**：当前目录无 manifest 时，退出码 1，提示 `Not an agent-cli project. Run 'agent-cli init <name>' first.`

---

### 2.4 `agent-cli-manifest.yaml` schema（C4）

由 `init` 命令生成，写在项目根目录。

```yaml
# agent-cli-manifest.yaml
schema_version: 1
name: xiaohongshu-trend-agent
template:
  name: agentscope
  version: 0.1.0
agent_directory: src/agent
cli_version: 0.2.0
created_at: 2026-05-22T10:30:00+08:00
# 以下字段 MVP-2 留占位，Roadmap 填充：
# deployment_target: null  # bailian-app | fc-agentrun | sae | none
# eval:
#   evalsets_dir: tests/evalsets
```

`schema_version` 用于未来 `agent-cli scaffold upgrade` 的版本兼容判断。

---

## 3. Skill 层规格（4 个 SKILL.md）

### 3.1 写作策略：基于 Google 4 SKILL.md 改写

**Quest 必须先 fetch Google 仓库的对应 SKILL.md 作为骨架**，再按下表本地化：

| 我们的 Skill | Google 源文件 | 改写工作量 |
|---|---|---|
| `agent-cli-alicloud-workflow` | `skills/google-agents-cli-workflow/SKILL.md` | **结构性重写**：保留 lifecycle 章节框架；**新增 Phase 0 "Idea→Design 引导"**（5 澄清问题 + AGENTS.md 写作要点 + scope.md 模板）；删除 ADK / Vertex 相关段落 |
| `agent-cli-alicloud-scaffold` | `skills/google-agents-cli-scaffold/SKILL.md` | **本地化替换**：命令名 `agents-cli create/enhance/upgrade` → `agent-cli init`（MVP-2 只有 init）；目录结构改成 AgentScope 兼容；保留 manifest 章节 |
| `agent-cli-alicloud-deploy` | `skills/google-agents-cli-deploy/SKILL.md` | **结构性重写**：保留"决策树"章节框架；目标平台改为 百炼应用 / 函数计算 AgentRun / SAE 三选一；提及 AgentScope `deploy()` 一键打包；MVP-2 仅决策方法论，无实际命令 |
| `agent-cli-alicloud-eval` | `skills/google-agents-cli-eval/SKILL.md` | **本地化替换**：保留 evalset / LLM-as-judge / trajectory 三段；改为 AgentScope eval harness 语境；MVP-2 仅方法论，无 `agent-cli eval run` 命令 |

**Google 源仓库**：`/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/agents-cli/skills/`（已克隆在本地）。

**4 步本地化方法（每个 SKILL.md 都要走）**：

1. **Frontmatter 重写**：`name: agent-cli-alicloud-{x}`，`description` 改中文 + 阿里云语境
2. **命令硬替换**：`agents-cli` → `agent-cli`；`gcloud` 段整段删除或换"阿里云 OpenAPI 占位（Roadmap）"
3. **云组件硬替换**：Cloud Run / GKE / Vertex AI / Agent Runtime → 函数计算 / AgentRun / SAE / 百炼
4. **不照搬 Google 没说但我们要说的**：每个 SKILL 末尾必须有 `## When to switch to another skill` 段，列出何时让 Coding Agent 切到下一个 Skill

### 3.2 workflow Skill 必须包含的内容（MVP-2 关键差异化 Pillar B）

`agent-cli-alicloud-workflow/SKILL.md` 必须有以下章节：

- `## Phase 0: Idea Clarification`（**Google 没有的部分**）
  - 5 个澄清问题模板（终端用户 / 触发方式 / 输入数据 / 输出形态 / 合规边界）
  - 默认答案兜底（用户拒答时怎么办）
- `## Phase 1: Design Documents`（**Google 没有的部分**）
  - AGENTS.md 写作要点（含 Project Identity / Single Core Interaction / Tech Stack / Data Flow / Compliance 五段）
  - scope.md 模板（IN / OUT / Feature Amendment）
  - eval-plan.md 思路（5 维度评分 + 通过门槛）
- `## Phase 2: Scaffold`（薄）
  - "走完 Phase 0/1 后，调 `agent-cli init <name> --template agentscope`"
  - 切到 scaffold Skill 的触发条件
- `## Phase 3: Implementation Pointers`（薄）
  - main.py 该写什么
  - 何时切到 deploy / eval Skill
- `## Reference: Pillar A/B/C 不许偏离`
  - 复述 AGENTS.md 三支柱

### 3.3 其他 3 个 Skill 的最低交付

每个 SKILL.md 至少 60 行，frontmatter + 大纲完整，关键章节有内容（不是 TODO 占位）。允许部分细节段落标 `> Roadmap: 详细命令规格在 MVP-3 填充`，但不能整个 skill 都是 TODO。

---

## 4. 仓库目录结构（产出件）

```
agent-cli-alicloud/                              # 本项目根（与 founder-playbook/ 同级，但本项目要发布的是这个目录）
├── pyproject.toml                              # uv + typer + jinja2 + pyyaml；不依赖任何 LLM SDK
├── README.md                                   # 5 分钟 quickstart（中文）
├── install.sh                                  # GitHub clone 用户的本地安装脚本
├── Makefile                                    # make verify = pytest + ruff + mypy
├── ruff.toml
├── .python-version                             # 3.11
├── src/agent_cli_alicloud/
│   ├── __init__.py
│   ├── __main__.py                             # python -m agent_cli_alicloud
│   ├── cli.py                                  # typer app: setup / init / info
│   ├── core/
│   │   ├── __init__.py
│   │   ├── manifest.py                         # 读写 agent-cli-manifest.yaml
│   │   ├── detector.py                         # 检测 4 种 Coding Agent skills 目录
│   │   ├── scaffold.py                         # jinja2 渲染 templates/agentscope/*
│   │   └── installer.py                        # setup 命令把 skills/ 复制到目标
│   ├── templates/
│   │   └── agentscope/
│   │       ├── pyproject.toml.j2
│   │       ├── README.md.j2
│   │       ├── env.example.j2                  # .env.example
│   │       ├── manifest.yaml.j2                # agent-cli-manifest.yaml
│   │       └── src/
│   │           ├── agent/__init__.py.j2
│   │           ├── agent/main.py.j2
│   │           └── agent/tools/__init__.py.j2
│   │           └── agent/tools/placeholder.py.j2
│   │       └── tests/test_main.py.j2
│   └── skills/                                 # 内嵌的 4 个 SKILL.md（也作为 setup 的源）
│       ├── agent-cli-alicloud-workflow/SKILL.md
│       ├── agent-cli-alicloud-scaffold/SKILL.md
│       ├── agent-cli-alicloud-deploy/SKILL.md
│       └── agent-cli-alicloud-eval/SKILL.md
└── tests/
    ├── conftest.py
    ├── test_cli_setup.py                       # setup 命令单测（mock home 目录）
    ├── test_cli_init.py                        # init 命令单测
    ├── test_cli_info.py                        # info 命令单测
    ├── test_manifest.py                        # manifest 读写单测
    ├── test_detector.py                        # 检测器单测
    └── golden/
        └── xiaohongshu_demo/
            ├── expected_tree.txt               # 期望的目录结构
            ├── expected_manifest.yaml          # 期望的 manifest 内容
            ├── expected_pyproject.toml         # 期望的 pyproject.toml（snapshot）
            └── expected_main.py                # 期望的 src/agent/main.py（snapshot）
```

注意：`AGENTS.md` / `scope.md` / `eval-plan.md` **不在** `templates/agentscope/` 里，因为它们由用户的 Coding Agent 在 workflow Skill 引导下产出，不由 CLI 渲染。

---

## 5. Golden Snapshot 验收（C6）

**核心原则**：golden 测试**不依赖 LLM、不依赖网络、不依赖 DashScope API key**。任何 contributor 在离线环境下都能跑通。

### 5.1 验收命令

```bash
$ pytest -k golden -v
tests/golden/test_init_xiaohongshu.py::test_directory_tree PASSED
tests/golden/test_init_xiaohongshu.py::test_manifest_content PASSED
tests/golden/test_init_xiaohongshu.py::test_pyproject_snapshot PASSED
tests/golden/test_init_xiaohongshu.py::test_main_py_snapshot PASSED
```

### 5.2 测试内容

```python
# tests/golden/test_init_xiaohongshu.py 必须实现的 4 个 case
def test_directory_tree(tmp_path):
    # 跑 agent-cli init xiaohongshu-trend-agent --dir tmp_path
    # 比对 tmp_path / xiaohongshu-trend-agent 下的文件树 == expected_tree.txt
    ...

def test_manifest_content(tmp_path):
    # 比对 manifest YAML（除了 created_at 字段）与 expected_manifest.yaml 一致
    ...

def test_pyproject_snapshot(tmp_path):
    # 比对生成的 pyproject.toml == expected_pyproject.toml
    ...

def test_main_py_snapshot(tmp_path):
    # 比对 src/agent/main.py == expected_main.py（应该是 AgentScope 兼容的 echo agent）
    ...
```

### 5.3 main.py 最小实现要求

生成的 `src/agent/main.py` 必须：
- import AgentScope（即使 AgentScope 未实际安装也要能 import-time 不挂；用 try/except 兜底）
- 定义一个最简 echo agent class（继承 AgentScope agent 抽象，方法返回输入原文）
- 包含 `if __name__ == "__main__":` 入口，`uv run python -m agent.main "美妆品类"` 能跑出 mock 输出
- **不**调用任何 LLM API（main.py 是脚手架占位，真实业务由用户的 Coding Agent 后续填充）

---

## 6. Demo 验收路径（D1-D4）

按 `scope.md` v0.2 §1.3 的 D1-D4 验收。Quest 完工后必须人工跑一遍三方协作流程：

1. **D1 setup**：跑 `uvx agent-cli-alicloud setup` 或 `./install.sh && agent-cli setup`，确认 Qoder 的 `~/.qoder/skills/` 下出现 4 个 SKILL.md
2. **D2 Idea→Design**：在 Qoder 中说"我想做一个能帮品牌方分析小红书爆文的 Agent，请用 agent-cli-alicloud"，确认 Qoder 自动加载 workflow Skill 并问出 5 个澄清问题
3. **D3 init**：让 Qoder 调 `agent-cli init xiaohongshu-trend-agent`，确认骨架生成正常
4. **D4 golden**：跑 `pytest -k golden`，全绿

---

## 7. Quest 验收清单

- [ ] `uv sync && uv run agent-cli --help` 显示三个子命令 setup / init / info
- [ ] `uv run agent-cli setup` 在测试 home 目录下能装 4 个 skill
- [ ] `uv run agent-cli init test-project` 生成第 4 节描述的目录树
- [ ] `uv run agent-cli info`（在 init 出来的目录里跑）输出项目信息
- [ ] `pytest -k golden` 通过
- [ ] `uv run pytest`（含非 golden）通过
- [ ] `uv run ruff check` 零错误
- [ ] `uv run mypy src/agent_cli_alicloud/core` 零错误
- [ ] **`grep -r "dashscope\|openai\|httpx\|requests" src/agent_cli_alicloud/` 无业务代码命中**（核心红线：CLI 不依赖 LLM SDK / 网络库）
- [ ] 4 个 SKILL.md 已基于 Google 对应文件改写完成，每个 ≥ 60 行，frontmatter 完整
- [ ] workflow SKILL.md 含 Phase 0 (Idea Clarification) 和 Phase 1 (Design Documents) 两个 Google 没有的章节
- [ ] README 写有 5 分钟 quickstart 演示三方协作流程
- [ ] SESSION-LOG.md 末尾追加本次 session 记录

---

## 8. 给 Quest 的实施提示（IMPORTANT）

**红线规则（违反任何一条都不许 commit）**：

1. `src/agent_cli_alicloud/` 下**禁止**出现 `import openai` / `import dashscope` / `import httpx` / `import requests` 等 LLM/网络相关 import（installer.py 用 `shutil.copy` 即可，不需网络）
2. `templates/agentscope/` 下的 `.j2` 模板**禁止**出现 LLM prompt 字符串 / API key 引用
3. **不要**自创 `AGENTS.md.j2` / `scope.md.j2` / `eval-plan.md.j2`——这些是 Coding Agent 产出的，不是 CLI 产出的
4. **不要**保留 v0.1 spec 中的 `core/llm.py` / `prompts/` 目录 / `init_flow.py`
5. typer 命令必须用 `Annotated[str, typer.Argument(...)]` / `Annotated[str, typer.Option(...)]` 写参数；不要裸 `str`
6. 错误信息中文 + `建议: ...` 后缀
7. 所有用户可见输出**中文**（除命令名 / 选项 / 文件名 / Python 代码）

**复用 v0.1 已写的代码**（在 `archive/legacy-route-a-v0.1` 分支）：
- ✅ 可复用：`pyproject.toml`、`ruff.toml`、`Makefile`、`.python-version`、`tests/conftest.py`、`__main__.py` 骨架、CI 配置
- ❌ 必须丢弃：`init_flow.py`、`core/llm.py`、`prompts/*`、依赖 LLM 的 jinja2 模板、调 LLM 的 golden fixture

**Skill 改写参考路径**：Google 源文件在 `/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/agents-cli/skills/google-agents-cli-{workflow,scaffold,deploy,eval}/SKILL.md`，请逐个 copy → rename → localize。

**Repo wiki 引用**（Citation 已开）：
- `.qoder/repowiki/zh/content/技术架构.md` — 学 CLI + Skills + Cloud Adapter 三层
- `.qoder/repowiki/zh/content/项目管理命令.md` — 学 setup / create / info 命令的设计模式
- `.qoder/repowiki/zh/content/技能-Skills/Workflow-技能.md` — 学 workflow Skill 的章节组织
- `.qoder/repowiki/zh/content/技能-Skills/Scaffold-技能.md` — 学 scaffold Skill 与 manifest 的协作

**禁止修改**：`/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/agents-cli/`（Google 源仓库，作为只读参考）。

---

## 9. 与 v0.1 的差异速查表（给 Quest 看）

| 维度 | v0.1（旧） | v0.2（本文件） |
|---|---|---|
| init 命令输入 | `"<idea 一句话>"` | `<name>` 项目名 |
| init 是否调 LLM | 是 | **否** |
| init 是否生成设计文档 | 生成 AGENTS.md/scope.md/eval-plan.md | **不生成**（由 Coding Agent + Skill 产出） |
| 命令面 | `init` 一条 | `setup` / `init` / `info` 三条 |
| Skills 数量 | 1 个真实 + 3 占位 | **4 个全部真实**（基于 Google 改写） |
| Skills 分发方式 | 无 | `agent-cli setup` 自动装到 4 种 Coding Agent |
| 状态文件 | 无 | `agent-cli-manifest.yaml` |
| 网络/LLM 依赖 | 强依赖 DashScope | **零依赖**（pyproject.toml 不含 LLM SDK） |
| Golden 测试是否需要 API key | 是 | **否**（纯模板渲染） |
| 验收红线 | 5 分钟跑通 | 5 分钟跑通 + 离线可跑 + 三方协作 demo 通过 |
