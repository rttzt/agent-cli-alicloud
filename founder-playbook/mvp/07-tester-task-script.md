# Step 7 测试者任务脚本

> **给测试者看的一页纸。** 请把本页发给你的朋友/同事，让他们照着走。
> 预计耗时 15-20 分钟（含反馈表）。
>
> [DEMO MODE] 真实创业里，这一步是"5 个目标用户亲手跑核心交互"。
> 我们当前用 3-5 个开发者朋友替代，重点练习"观察 → 记录 → 决策"的肌肉记忆。

---

## 你是谁？

你是一位会写 Python 的开发者。我们要测试一个 CLI 工具，它能帮你在阿里云上快速搭建 AI Agent 项目。

## 前提条件

- macOS 或 Linux
- 已安装 Python 3.11+ 和 [uv](https://docs.astral.sh/uv/)（`curl -LsSf https://astral.sh/uv/install.sh | sh`）
- 至少装有 Qoder / 通义灵码 / Claude Code / Cursor 中的任意一个
- 15-20 分钟空闲时间

---

## 测试任务（按顺序走）

### Task 1：安装 CLI（~1 分钟）

```bash
git clone https://github.com/rttzt/agent-cli-alicloud.git
cd agent-cli-alicloud
./install.sh
```

**记录**：
- [ ] 安装是否一次成功？
- [ ] 看到了什么输出？
- [ ] 有没有卡住的地方？

### Task 2：装 Skills 到你的 Coding Agent（~1 分钟）

```bash
agent-cli setup
```

**记录**：
- [ ] 检测到了你的哪些 Coding Agent？
- [ ] 显示装了几个 Skills？
- [ ] 有没有报错或看不懂的信息？

### Task 3：让 Coding Agent 引导你设计（~8 分钟）

打开你的 Coding Agent（Qoder / 灵码 / Claude Code / Cursor），对它说：

> "我想做一个小红书爆文分析 Agent，请用 agent-cli-alicloud"

你的 Coding Agent 应该会自动加载 `agent-cli-alicloud-workflow` Skill，然后引导你回答 5 个澄清问题，最后帮你生成设计文档（AGENTS.md / scope.md / eval-plan.md）。

**跟着 Agent 走完引导流程，记录**：
- [ ] Agent 是否自动识别并加载了 workflow Skill？
- [ ] 5 个澄清问题是否合理？你觉得哪个问题最难回答？
- [ ] 生成的 AGENTS.md 看起来像回事吗？有哪些明显的错误或缺失？
- [ ] 你觉得这个引导过程有价值吗？还是觉得多余？

### Task 4：生成项目骨架（~1 分钟）

在 Coding Agent 完成设计文档后，执行（或让 Agent 帮你执行）：

```bash
agent-cli init xiaohongshu-trend-agent --template agentscope
```

**记录**：
- [ ] 命令是否一次成功？
- [ ] 输出的目录结构看起来合理吗？
- [ ] 有没有你觉得缺少的文件？

### Task 5：查看项目状态（~30 秒）

```bash
cd xiaohongshu-trend-agent
agent-cli info
agent-cli info --format json
```

**记录**：
- [ ] text 和 json 两种格式是否都有输出？
- [ ] 信息是否有用？你能想到什么场景需要这个命令？

### Task 6：跑一下生成的 Agent（~2 分钟）

```bash
cd xiaohongshu-trend-agent
PYTHONPATH=src python3 -m agent.main "美妆品类"
```

**记录**：
- [ ] 是否有输出？输出内容像"分析报告"吗？
- [ ] 你注意到这是 Mock 模式吗？
- [ ] 如果要接真实的 LLM，你知道下一步该做什么吗？

### Task 7：填写反馈表（~5 分钟）

打开反馈表（`07-feedback-form.md`），逐项填写后发给我。

---

## 注意事项

- 这不是考试，没有"正确"答案。卡住了也是有价值的反馈——请记录卡在哪、为什么卡。
- 如果某一步你觉得完全没用，直接写"没用"就好，不需要委婉。
- 如果你跳过了某一步，请标注"跳过"和跳过的原因。
- 整个过程大约 15-20 分钟。
