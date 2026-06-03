# agent-cli-alicloud

阿里云 Agent 开发脚手架 CLI — CLI + Skills 双层架构。

## 快速开始（5 分钟）

### 安装

方式一：PyPI（推荐）
```bash
uvx agent-cli-alicloud setup
```

方式二：从源码
```bash
git clone https://github.com/rttzt/agent-cli-alicloud.git
cd agent-cli-alicloud
./install.sh
```

### 三方协作流程

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

### Step 1: 安装 Skills 到你的 Coding Agent
```bash
agent-cli setup
```

### Step 2: 在 Coding Agent 中开始对话
告诉你的 Coding Agent：
> "我想做一个小红书爆文分析 Agent，请用 agent-cli-alicloud"

Coding Agent 会自动加载 workflow Skill，引导你完成：
- 5 个澄清问题（终端用户、触发方式、输入数据、输出形态、合规边界）
- 生成 AGENTS.md / scope.md / eval-plan.md

### Step 3: 生成项目骨架
```bash
agent-cli init xiaohongshu-trend-agent --template agentscope
```

### Step 4: 开始开发
在生成的项目中，继续与 Coding Agent 协作填充业务逻辑。

## 命令参考

| 命令 | 功能 |
|---|---|
| `agent-cli setup` | 检测 Coding Agent 并安装 Skills |
| `agent-cli init <name>` | 生成 Agent 项目骨架 |
| `agent-cli info` | 展示项目状态 |

## 架构

- **CLI 层**（确定性执行）：不调 LLM、不发网络请求、可离线运行
- **Skill 层**（认知引导）：由用户的 Coding Agent 消费，引导完成设计工作

## 开发

```bash
uv sync
make verify  # pytest + ruff check + mypy
```
