# R1 Watchlist

> 监控阿里云生态里**会直接威胁我们 dev-time workflow 这条赛道**的官方动作。
> **触发条件**：任意一家明确推出"模糊想法 → 设计文档 → 脚手架"端到端工具，立即触发 Pivot 评估。
> 频率：创始人每两周 review 一次。

## 监控清单

| 来源 | 关注什么 | 监控方式 |
|---|---|---|
| AgentScope release notes | 是否新增"被 coding agent 消费的 Skill 包 / 设计模板 / 方法论文档" | github.com/agentscope-ai/agentscope/releases |
| 阿里云函数计算 AgentRun | 是否扩到 dev-time（目前只在 runtime 层） | aliyun.com/product/fc/agentrun + product/news |
| 百炼 ModelStudio | 是否新增"从想法→AGENTS.md/scope→脚手架"流程 | help.aliyun.com/zh/model-studio + 36kr/zhihu 报道 |
| 通义灵码 / Qoder CN | `create-agent` 是否扩到生成商业级 agent 项目骨架（而非 IDE 内置 agent） | help.aliyun.com/zh/lingma + 灵码博客 |
| Google `agents-cli` | 是否做中文化 / 阿里云适配 | github.com/google/agents-cli releases |

## 已确认**非威胁**（避免误监控）

- **百炼 workflow application** —— 是 runtime 节点编排器，与我们 dev-time skill 不在同一层（详见 03-evidence-pool §5）
- **Dify / FastGPT / Coze / n8n** —— 同上，全是 runtime 编排
- **AgentScope `deploy()`** —— 是部署端便捷化，不进 dev-time

## Pivot 触发后的步骤

1. 立即新建 `founder-playbook/05-pivot-review-vYY-MM-DD.md`
2. 重做 02 (Competitive Landscape) 的 §5 三根支柱位置
3. 重新评估 MVP 切片是否仍然成立
4. ≥2 个 Pillar 失守 ⇒ 必须 Pivot；1 个 Pillar 失守 ⇒ 收窄继续

---

*更新：每次 review 在文件末尾加一条 `## YYYY-MM-DD review` 记录扫描结果（无变化也要写"无变化"）。*
