---
name: agent-cli-alicloud-scaffold
description: >
  当用户想要"创建 Agent 项目"、"初始化项目骨架"、"生成 AgentScope 项目"时使用此技能。
  覆盖 `agent-cli init` 命令的使用方式、模板选项、目录结构说明。
  不用于编写 Agent 代码（使用 agent-cli-alicloud-workflow Phase 3）或
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

# AgentScope 项目脚手架指南

> **依赖：** `agent-cli`（`uvx agent-cli-alicloud setup` 安装）

使用 `agent-cli init` 命令创建 AgentScope 兼容的 Agent 项目骨架。纯模板渲染，不调用 LLM、不发网络请求。

---

## 前置条件：先澄清需求（新项目必须）

**创建新项目前，先加载 `/agent-cli-alicloud-workflow` 完成 Phase 0**——澄清用户的需求再执行脚手架命令。确认用户想做什么 Agent、需要什么工具、目标用户是谁。

---

## Step 1: 创建项目

```bash
agent-cli init <project-name> --template agentscope
```

**约束：**
- 项目名称必须小写字母开头，仅含小写字母、数字和连字符，长度 2-64
- 不要在执行 `init` 前手动 `mkdir`——CLI 会自动创建目录
- 使用 `--dir` 指定输出到非当前目录
- 使用 `--force` 覆盖已存在的目录

### 命令选项

| 选项 | 说明 |
|------|------|
| `--template`, `-t` | 项目模板（当前仅支持 `agentscope`） |
| `--dir`, `-d` | 输出目录（默认当前目录） |
| `--force`, `-f` | 覆盖已存在的目录 |

---

## Step 2: 生成的目录结构

```
{project-name}/
├── pyproject.toml              # 项目配置（AgentScope 依赖）
├── README.md                   # 项目说明
├── .env.example                # 环境变量模板
├── agent-cli-manifest.yaml     # CLI 元数据（勿删）
├── src/agent/
│   ├── __init__.py
│   ├── main.py                 # Agent 入口（EchoAgent 占位）
│   └── tools/
│       ├── __init__.py
│       └── placeholder.py      # 占位工具
└── tests/
    └── test_main.py            # 基础测试
```

### 关键文件说明

- **`src/agent/main.py`** — Agent 主入口，默认是 EchoAgent（原样返回输入）。真实业务逻辑由 Coding Agent 在 workflow Skill 引导下填充。
- **`agent-cli-manifest.yaml`** — CLI 读取的项目元数据，不要手动删除或修改。
- **`.env.example`** — 环境变量模板，复制为 `.env` 并填入 API Key。

---

## Step 3: 后续步骤

项目创建后，立即加载 `/agent-cli-alicloud-workflow` Phase 3，开始实现 Agent 逻辑：

1. 替换 `src/agent/main.py` 中的 EchoAgent
2. 在 `src/agent/tools/` 添加自定义工具
3. 配置 `.env` 中的 LLM API Key
4. 运行 `uv run pytest` 验证

---

## 模板选项

| 模板 | 说明 |
|------|------|
| `agentscope` | AgentScope 兼容项目（默认，当前唯一） |

> **Roadmap:** 未来版本将支持 `langchain`、`llamaindex` 等模板。

---

## 常见问题

### 项目名称不合法

项目名称必须匹配 `^[a-z][a-z0-9-]{1,63}$`：
- 小写字母开头
- 仅含小写字母、数字、连字符
- 长度 2-64 字符

### 目录已存在

使用 `--force` 覆盖，或选择其他输出目录。

### `agent-cli` 命令未找到

运行 `uvx agent-cli-alicloud setup` 安装 CLI。

---

## Critical Rules

- **不要跳过需求澄清** — 先走 `/agent-cli-alicloud-workflow` Phase 0
- **不要手动 mkdir** — CLI 自动创建目录
- **不要修改 manifest** — `agent-cli-manifest.yaml` 由 CLI 管理
- **从 Prototype 开始** — 先让 Agent 跑起来再考虑部署

---

## When to switch to another skill

| 场景 | 切换到 |
|------|--------|
| 需要澄清需求或生成设计文档 | `/agent-cli-alicloud-workflow` |
| 需要评估 Agent 行为质量 | `/agent-cli-alicloud-eval` |
| 需要部署到阿里云 | `/agent-cli-alicloud-deploy` |

---

## Related Skills

- `/agent-cli-alicloud-workflow` — 开发工作流、想法澄清、设计文档生成
- `/agent-cli-alicloud-eval` — 评估方法论与评分体系
- `/agent-cli-alicloud-deploy` — 部署到阿里云（函数计算 / AgentRun / SAE）
