# agent-cli-alicloud

让任意 Coding Agent 把一句模糊的 Agent 想法，5 分钟内变成结构化设计文档 + 可运行的脚手架。

## 5 分钟 Quickstart

### 安装

```bash
# 方式一：通过 uvx 直接运行（推荐）
uvx agent-cli-alicloud init "你的 Agent 想法"

# 方式二：从 GitHub 安装
git clone <repo-url>
cd agent-cli-alicloud
./install.sh
```

### 运行

```bash
agent-cli init "我想做一个能帮品牌方分析小红书爆文的 Agent"
```

### 运行效果

命令会自动执行 4 个步骤：

1. **[1/4] 澄清问题** — 生成 5 个澄清问题，帮你理清需求
2. **[2/4] 设计文档** — 生成 AGENTS.md、scope.md、eval-plan.md
3. **[3/4] 项目脚手架** — 生成 AgentScope 兼容的 Python 项目骨架
4. **[4/4] 下一步** — 生成 next-steps.md，列出交给 Coding Agent 的具体任务

### 输出目录结构

```
./your-agent-project/
├── AGENTS.md          # 项目设计文档
├── scope.md           # 范围定义
├── eval-plan.md       # 评测计划
├── clarification.md   # 澄清问答记录
├── next-steps.md      # 下一步行动
├── pyproject.toml
├── src/agent/
│   ├── main.py        # Agent 入口
│   └── tools/         # 工具占位
└── tests/
    └── test_main.py
```

## 开发

```bash
# 安装依赖
cd agent-cli-alicloud
uv sync --all-extras

# 运行测试
uv run pytest

# 代码检查
uv run ruff check
uv run mypy src/agent_cli_alicloud/core
```

## Tech Stack

| 层 | 选型 |
|---|---|
| 语言 | Python 3.11+ |
| 项目管理 | uv |
| CLI 框架 | typer |
| 模板引擎 | jinja2 |
| LLM | DashScope / Qwen |
| 测试 | pytest |

## 许可

Apache-2.0
