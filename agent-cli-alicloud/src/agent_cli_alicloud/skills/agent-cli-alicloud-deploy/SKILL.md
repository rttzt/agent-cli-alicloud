---
name: agent-cli-alicloud-deploy
description: >
  当用户想要"部署 Agent"、"上线 Agent"、"发布到阿里云"、"配置函数计算"、
  "使用 AgentRun 部署"时使用此技能。覆盖阿里云部署目标决策方法论：
  函数计算（FC）、AgentRun、SAE（Serverless 应用引擎）。
  MVP 阶段仅提供决策方法论和 Roadmap，不包含实际部署命令实现。
  不用于编写 Agent 代码（使用 agent-cli-alicloud-workflow）或
  评估（使用 agent-cli-alicloud-eval）。
metadata:
  author: agent-cli-alicloud
  license: Apache-2.0
  version: 0.2.0
  requires:
    bins:
      - agent-cli
    install: "uvx agent-cli-alicloud setup"
---

# 阿里云 Agent 部署指南

> **当前状态：** MVP 阶段——本技能提供部署决策方法论和 Roadmap。实际部署命令（`agent-cli deploy`）将在后续版本实现。

> **依赖：** `agent-cli`（`uvx agent-cli-alicloud setup` 安装）

---

## 部署目标决策矩阵

根据需求选择合适的阿里云部署目标：

| 维度 | 函数计算（FC） | AgentRun | SAE |
|------|---------------|----------|-----|
| **语言** | Python / Node.js / Go / Java | Python | Python / Java / Go / Node.js |
| **弹性伸缩** | 全托管（按量付费，闲时零成本） | 托管自动伸缩 | 配置式自动伸缩 |
| **会话状态** | 无状态（需外部存储） | 内置会话管理 | 需自行管理 |
| **事件驱动** | 原生支持（OSS / MNS / 定时触发） | 对话触发 | HTTP 触发 |
| **费用模型** | 按调用次数 + 执行时长 | 按 vCPU-小时 + 内存 | 按实例规格 + 运行时长 |
| **运维复杂度** | 低（全托管） | 低（Agent 专用托管） | 中（容器化部署） |
| **最佳场景** | 事件驱动、短时任务、高并发 | 对话式 Agent、多轮交互 | 长运行服务、自定义运行时 |

### 何时选择什么

- **对话式 Agent + 想最快上线** → AgentRun（推荐）
- **事件驱动 / 定时任务 / 轻量函数** → 函数计算
- **需要自定义运行时 / 长连接 / WebSocket** → SAE
- **百炼应用商店发布** → 先部署到 AgentRun，再注册到百炼

---

## 部署前检查清单

在考虑部署前，确认：

1. ✅ Agent 代码在本地可运行（`uv run python -m agent.main "测试"`）
2. ✅ 评估通过（参见 `/agent-cli-alicloud-eval`）
3. ✅ 环境变量已配置（`.env` 中的 API Key）
4. ✅ 合规红线已确认（参见 AGENTS.md Compliance 段）

---

## 百炼应用发布（Roadmap）

将 Agent 注册到百炼应用商店，使其可被其他用户/系统调用：

1. Agent 部署到 AgentRun
2. 在百炼控制台注册应用
3. 配置 API 权限和调用限额
4. 发布上线

> **阿里云 OpenAPI 占位（Roadmap）：** 未来版本将支持通过 CLI 自动化上述流程。

---

## 环境变量与密钥管理

**推荐方案：** 使用阿里云密钥管理服务（KMS）管理敏感信息。

```bash
# 本地开发：.env 文件
DASHSCOPE_API_KEY=your-api-key

# 生产部署：通过环境变量注入（KMS 托管）
# FC: 函数配置 → 环境变量
# SAE: 应用配置 → 环境变量
# AgentRun: 平台配置
```

---

## 部署架构概览

```
用户请求
  │
  ▼
┌─────────────────┐
│  API 网关       │  ← 可选：流量管理、鉴权
├─────────────────┤
│  部署目标       │  ← FC / AgentRun / SAE
├─────────────────┤
│  Agent 代码     │  ← AgentScope + 自定义工具
├─────────────────┤
│  LLM 服务      │  ← DashScope（通义千问）
├─────────────────┤
│  外部数据源     │  ← 数据库 / OSS / 第三方 API
└─────────────────┘
```

---

## Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| API Key 无效 | 检查 DashScope 控制台是否已开通、Key 是否过期 |
| 函数超时 | 增加 FC 超时配置（默认 60s，Agent 对话建议 120s+） |
| 内存不足 | 增加函数/应用内存配置 |
| 冷启动慢 | FC 使用预留实例；SAE 设置最小实例数 > 0 |
| 网络不通 | 检查 VPC 配置和安全组规则 |

---

## When to switch to another skill

| 场景 | 切换到 |
|------|--------|
| 需要从头开始设计 Agent | `/agent-cli-alicloud-workflow` |
| 需要创建项目骨架 | `/agent-cli-alicloud-scaffold` |
| 需要评估 Agent 行为质量 | `/agent-cli-alicloud-eval` |

---

## Related Skills

- `/agent-cli-alicloud-workflow` — 开发工作流、想法澄清、设计文档生成
- `/agent-cli-alicloud-scaffold` — 项目创建与脚手架生成
- `/agent-cli-alicloud-eval` — 评估方法论与评分体系
