# Qoder Quest MVP-2 开场指令（v0.2 — CLI + Skills 双层架构）

> 把下面整段复制粘贴到 Qoder Quest 新任务的第一条消息。

---

你是一个专家组，正在开发 **agent-cli-alicloud** 项目。本项目采用 **CLI + Skills 双层架构**（对标 Google `agents-cli`），CLI 层是确定性薄壳，Skill 层是认知载体。

## 核心铁律（最高优先级）

1. **CLI 层永不调 LLM、永不发网络请求**——`src/agent_cli_alicloud/` 下禁止出现 `import openai` / `import dashscope` / `import httpx` / `import requests`
2. **设计文档（AGENTS.md / scope.md / eval-plan.md）由 Coding Agent + Skill 引导产出**——CLI 的 `init` 命令只生成项目骨架和 manifest，不生成任何设计文档
3. **4 个 SKILL.md 必须基于 Google 对应文件改写**，不自创
4. **不修改 `agents-cli/` 目录下的任何文件**（只读参考）

---

## Pre-flight（必须先做，不跳步）

1. 读完项目根目录的 `AGENTS.md`
2. 读 `founder-playbook/mvp/scope.md`（特别是 §1 IN SCOPE 双层划分 + §2 OUT SCOPE 防火墙）
3. 读 `founder-playbook/mvp/01-mvp-spec.md`（**你的完整验收规格，v0.2**）
4. 读 `founder-playbook/mvp/SESSION-LOG.md` 末尾 3 条

---

## 参考架构（必须引用 Repo Wiki）

本项目根目录下有 `agents-cli/` 子目录 = Google 开源 agents-cli（github.com/google/agents-cli），是直接对标物。

### 必读 Wiki 页面（`.qoder/repowiki/zh/content/`）

| 页面 | 学什么 | 落地到我们的什么 |
|---|---|---|
| `项目概述/技术架构.md` | CLI + Skills + Cloud Adapter 三层 | `cli.py → core/ → skills/ → templates/` 骨架 |
| `CLI 命令参考/项目管理命令.md` | `scaffold create` 命令设计范式 | `agent-cli init` 体验对标 |
| `技能系统详解/Workflow 技能.md` | Phase 0→7 lifecycle | `workflow/SKILL.md` Phase 0/1 重写 |
| `技能系统详解/Scaffold 技能.md` | 原型优先 + manifest 协作 | `scaffold/SKILL.md` 本地化 |
| `核心概念/技能系统原理.md` | Skills 作为知识载体 | SKILL.md frontmatter + 章节规范 |
| `开发指南/项目结构与最佳实践.md` | 项目组织 | 目录结构参考 |

**引用方式**：当代码设计参考了 wiki 某页，在代码注释写 `# 参考 wiki: <页面路径>`。

### 差异化原则

- Google = GCP + ADK + Gemini CLI；**我们 = 阿里云 + AgentScope + 百炼 + 跨 Coding Agent**
- Google 侧重后半段 scaffold→deploy→observe；**我们加强前半段 Idea→Design**（Pillar B）
- Google 绑 Gemini CLI；**我们跨 Qoder/灵码/Claude Code/Cursor**（Pillar C）

---

## 你的 MVP-2 唯一目标

交付 **3 个 CLI 命令 + 4 个 SKILL.md**，使三方协作 demo 跑通：

```
用户                Coding Agent                     agent-cli
 │                        │                              │
 ├─ $ agent-cli setup ──────────────────────────────────▶│
 │                        │◀── Skills 装入 IDE ──────────┤
 │                        │                              │
 ├─"我想做小红书爆文 Agent" ─▶│                              │
 │                        ├─读 workflow Skill             │
 │                        ├─走 5 个澄清问题              │
 │                        ├─生成 AGENTS.md/scope.md/eval  │
 │                        │                              │
 │                        ├─ $ agent-cli init <name> ───▶│
 │                        │◀── 骨架 + manifest ──────────┤
 │                        │                              │
 │                        ├─ $ agent-cli info ──────────▶│
 │                        │◀── 项目状态 ─────────────────┤
 ▼                        ▼                              ▼
```

详细验收规格在 `founder-playbook/mvp/01-mvp-spec.md` v0.2，**请完整读完后再动手**。

---

## 工作目录

根目录：`/Users/weichang/qoder_demo/AGENT_CLI_Alicloud`

代码放在根目录下 `agent-cli-alicloud/` 子目录（与 `agents-cli/` 和 `founder-playbook/` 平级）。

---

## 步骤概览

### 1. 初始化项目骨架

```bash
cd /Users/weichang/qoder_demo/AGENT_CLI_Alicloud
mkdir -p agent-cli-alicloud && cd agent-cli-alicloud
uv init --name agent-cli-alicloud
```

### 2. 配置依赖（按 AGENTS.md §Tech Stack — 注意：不含任何 LLM SDK）

- `typer[all]`（CLI 框架）
- `jinja2`（模板引擎）
- `pyyaml`（manifest 读写）
- `pytest` + `pytest-asyncio`（测试）
- `ruff`（lint/format，dev only）
- `mypy`（类型检查 core/，dev only）

**⚠️ 禁止添加 `dashscope` / `openai` / `httpx` / `requests` 或任何 LLM/HTTP 库**

### 3. 搭目录骨架（详见 01-mvp-spec.md §4）

```
agent-cli-alicloud/
├── pyproject.toml
├── README.md
├── install.sh
├── Makefile                              # make verify = pytest + ruff + mypy
├── ruff.toml
├── .python-version                       # 3.11
├── src/agent_cli_alicloud/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                            # typer app: setup / init / info
│   ├── core/
│   │   ├── __init__.py
│   │   ├── manifest.py                   # 读写 agent-cli-manifest.yaml
│   │   ├── detector.py                   # 检测 4 种 Coding Agent skills 目录
│   │   ├── scaffold.py                   # jinja2 渲染 templates/agentscope/*
│   │   └── installer.py                  # setup: shutil.copy skills 到目标
│   ├── templates/agentscope/             # init 的 jinja2 模板
│   └── skills/                           # 4 个 SKILL.md（setup 的源）
│       ├── agent-cli-alicloud-workflow/SKILL.md
│       ├── agent-cli-alicloud-scaffold/SKILL.md
│       ├── agent-cli-alicloud-deploy/SKILL.md
│       └── agent-cli-alicloud-eval/SKILL.md
└── tests/
    ├── conftest.py
    ├── test_cli_setup.py
    ├── test_cli_init.py
    ├── test_cli_info.py
    ├── test_manifest.py
    ├── test_detector.py
    └── golden/xiaohongshu_demo/
```

### 4. 实现 3 个 CLI 命令

按 `01-mvp-spec.md` §2 逐个实现：
- `agent-cli setup` — 检测 Coding Agent + 复制 Skills
- `agent-cli init <name> [--template agentscope]` — jinja2 渲染骨架 + 写 manifest
- `agent-cli info` — 读 manifest 展示项目状态

### 5. 改写 4 个 SKILL.md

**必须先 fetch Google 源文件再改写**：

```bash
# Google 源（本地只读）
ls /Users/weichang/qoder_demo/AGENT_CLI_Alicloud/agents-cli/skills/
# → google-agents-cli-workflow/  google-agents-cli-scaffold/  google-agents-cli-deploy/  google-agents-cli-eval/  ...
```

按 `01-mvp-spec.md` §3 的 4 步本地化方法逐个改写。**workflow SKILL.md 的 Phase 0 和 Phase 1 是 Google 没有的，必须新写**。

### 6. Golden Snapshot 测试

按 `01-mvp-spec.md` §5 写 4 个 test case（directory tree / manifest / pyproject / main.py），确保**不依赖 LLM / 不依赖网络**。

### 7. README + install.sh

README 含 5 分钟 quickstart 展示三方协作流程（setup → Coding Agent 读 Skill → init → 开发）。

---

## 验收清单（全绿才算 done — 逐条跑！）

```bash
# 基础
uv sync && uv run agent-cli --help

# 命令跑通
uv run agent-cli setup                    # 在 mock home 下测试
uv run agent-cli init test-project        # 生成骨架
cd test-project && uv run agent-cli info  # 读 manifest

# 质量
uv run pytest                              # 含 golden + 非 golden 全过
uv run pytest -k golden -v                 # golden 专项
uv run ruff check                          # 零错误
uv run mypy src/agent_cli_alicloud/core    # 零错误

# 红线
grep -r "dashscope\|openai\|httpx\|requests" src/agent_cli_alicloud/
# ↑ 此命令必须无业务代码命中（只允许注释里出现）

# Skills 完整性
find src/agent_cli_alicloud/skills -name "SKILL.md" | wc -l
# ↑ 必须等于 4
```

---

## 约束提醒（违反 = 拒绝合并）

- ❌ CLI 代码里调 LLM / 发网络请求
- ❌ 让 `init` 命令生成 AGENTS.md / scope.md / eval-plan.md
- ❌ 自创 SKILL.md 内容而不基于 Google 源文件改写
- ❌ 修改 `agents-cli/` 目录下的任何文件
- ❌ 在 pyproject.toml 添加 LLM SDK 依赖
- ❌ Golden 测试依赖外部 API 或网络
- ❌ 自行扩 scope（写进 `SCOPE-PROPOSALS.md` 等创始人审批）
- ✅ 用 `Annotated[str, typer.Argument(...)]` 写 typer 参数
- ✅ 用户可见文案中文（命令名/选项/文件名/代码除外）
- ✅ 错误信息格式 `…，建议：…`
- ✅ 代码注释标注 wiki 参考来源

---

## Post-flight

1. 在 `founder-playbook/mvp/SESSION-LOG.md` 追加记录
2. 若本次让 `AGENTS.md` 失真，先更新 `AGENTS.md` 再 commit
3. 跑 `make verify`，失败禁止结束

开始吧。
