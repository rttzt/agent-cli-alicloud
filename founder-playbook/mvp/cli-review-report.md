# agent-cli-alicloud v0.2.0 深度 Review 报告

> 审查日期：2026-05-28
> 审查范围：CLI 命令（setup/init/info）+ 4 个 SKILL.md + 测试 + 生成产物

---

## 一、验收命令执行结果

| 命令 | 结果 | 详情 |
|------|------|------|
| `uv run pytest -v` | ✅ **48 passed in 0.16s** | 全部通过，含 golden + 集成 + 单元测试 |
| `uv run ruff check` | ✅ All checks passed | 零 lint 错误 |
| `uv run mypy src/agent_cli_alicloud/core` | ✅ Success: no issues found | 5 源文件类型检查通过 |
| `grep -rn "dashscope\|openai\|httpx\|requests" src/` | ✅ 仅 SKILL.md 文档引用 | Python 业务代码零命中 |
| `uv run agent-cli --help` | ✅ 正常输出 | 显示 setup/init/info/version 四命令 |
| `uv run agent-cli version` | ✅ `v0.2.0` | 版本号正确 |
| `agent-cli init` 生成项目 mock 运行 | ✅ 输出结构化分析报告 | 四维分析完整呈现 |

---

## 二、合规检查清单（v0.2 Spec 逐条对照）

| # | Spec 要求 | 状态 | 备注 |
|---|-----------|------|------|
| C1 | `setup` 检测 4 种 Coding Agent | ✅ | Qoder/灵码/Claude Code/Cursor 全部支持 |
| C2 | `init <name>` 纯 jinja2 渲染 | ✅ | 正则校验 `^[a-z][a-z0-9-]{1,63}$`，接受项目名不接受 idea |
| C3 | `info` 读 manifest 输出 | ✅ | 支持 text/json 两种格式 |
| C4 | `agent-cli-manifest.yaml` schema | ✅ | schema_version=1，含 name/template/agent_directory/cli_version/created_at |
| C5 | PyPI + install.sh 双轨分发 | ✅ | `uvx` 入口 + `install.sh` 均存在 |
| C6 | golden snapshot 测试 | ✅ | 4 个 golden test 全部通过 |
| S1 | workflow SKILL (Phase 0+1) | ✅ | 190 行，含 5 澄清问题 + 3 大设计文档模板 |
| S2 | scaffold SKILL | ✅ | 143 行，含命令选项 + 目录结构 + FAQ |
| S3 | deploy SKILL 占位 | ✅ | 138 行，含决策矩阵 + 架构图 |
| S4 | eval SKILL 占位 | ✅ | 180 行，含评估脚本示例 + 迭代方法论 |
| D1 | setup 分发 demo 路径 | ✅ | 安装到 `~/.qoder/skills/` 等 |
| D2 | Skill 引导设计文档 | ✅ | xiaohongshu-trend-agent 已生成 AGENTS.md/scope.md/eval-plan.md |
| D3 | init 生成骨架 | ✅ | 9 个文件 + manifest 均正确生成 |
| D4 | golden 不依赖 LLM | ✅ | 测试头声明 + 架构保证（零网络零 LLM） |

**合规结论：14/14 条全部通过。**

---

## 三、发现的问题与改进建议

### 3.1 严重问题（建议立即修复）

**[S1] `info --format` 参数无校验**
- 用户可传入 `--format xml` 等非法值，静默回退到 text 输出
- 修复：使用 `Literal["text", "json"]` 或手动校验

**[S2] `setup` 中 `install_skills()` 调用缺少异常捕获**
- 权限不足等 I/O 错误会导致未格式化的 traceback
- 修复：添加 try/except 并输出中文友好提示

**[S3] 生成项目 `xiaohongshu-trend-agent/tests/test_main.py` 硬编码绝对路径**
- 3 处出现 `/Users/weichang/qoder_demo/...` 绝对路径
- 导致测试无法在其他机器或 CI 上运行
- 修复：改用 `Path(__file__).parent.parent / "src"` 相对路径

### 3.2 中等问题（建议近期修复）

**[M1] `manifest.yaml.j2` 模板与 `write_manifest()` 冲突**
- scaffold 渲染模板后 cli.py 又调用 `write_manifest()` 覆写同一文件
- 模板文件变成无用代码
- 修复：删除模板或让 cli.py 不再重复写入

**[M2] `template_version` 硬编码 `"0.1.0"`**
- 与实际 CLI 版本 `0.2.0` 不一致
- 修复：从 `__init__.py` 的 `__version__` 读取或独立追踪

**[M3] Agent 检测仅靠目录存在性**
- 用户手动创建 `~/.qoder/skills/` 会被误判为已安装
- 修复：增加 `shutil.which()` 或配置文件存在性检测

**[M4] `typecheck` 目标不完整**
- Makefile 仅检查 `core/` 子目录，遗漏了 `cli.py`
- 修复：改为 `mypy src/agent_cli_alicloud/`

### 3.3 轻微问题（建议优化）

**[L1] `installer.py` 中 `dir`/`file` 分支执行相同代码**（冗余分支）
**[L2] `_AGENT_CONFIGS` 使用 `dict` 而非类型安全的 dataclass**
**[L3] `install.sh` 未检查 Python 版本**（项目要求 >= 3.11）
**[L4] `pytest-asyncio` dev 依赖可能冗余**（项目无 async 代码）
**[L5] 缺少 `--version` flag**（仅有 `version` 子命令）
**[L6] `scaffold.py` 的 `select_autoescape([])` 缺少注释说明**
**[L7] ruff 规则集偏基础**，建议添加 `UP`/`B`/`SIM`
**[L8] 缺少 `installer.py` 和 `scaffold.py` 的独立单元测试**

---

## 四、SKILL.md 质量评估

### 4.1 四文件总览

| Skill | 行数 | Frontmatter | 阿里云本地化 | Pillar B 内容 | "When to switch" |
|-------|------|-------------|-------------|---------------|-----------------|
| workflow | 190 | ✅ 完整 | ✅ 零 Google 残留 | ✅ Phase 0+1 | ✅ 4 场景 |
| scaffold | 143 | ✅ 完整 | ✅ 零 Google 残留 | N/A | ✅ 3 场景 |
| deploy | 138 | ✅ 完整 | ✅ 最充分的本地化 | N/A | ✅ 3 场景 |
| eval | 180 | ✅ 完整 | ✅ 零 Google 残留 | N/A | ✅ 3 场景 |

### 4.2 亮点

- workflow 的 Phase 0（5 澄清问题 + 默认兜底表）是比 Google 原版更好的设计
- deploy 的决策矩阵（7 维度 × 3 方案）和部署架构图非常实用
- eval 的 40 行可运行评估脚本示例和"评估 vs 单元测试"对比表是高价值内容

### 4.3 不足（相比 Google 原版缺失的有价值内容）

- workflow 缺少"代码保留原则"（Principle 1: Code Preservation & Isolation）
- workflow 缺少"系统调试方法论"（Systematic Debugging 5 步法）
- 缺少统一的命令速查表（Google 版有 20+ 命令汇总表）

---

## 五、代码质量评分

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 架构设计 | ⭐⭐⭐⭐⭐ | CLI/Skill 双层分离干净，模块划分清晰 |
| 类型安全 | ⭐⭐⭐⭐ | mypy strict + Annotated，但 config 用 dict |
| 错误处理 | ⭐⭐⭐½ | 大部分友好提示，但 install 缺 try/except |
| 测试覆盖 | ⭐⭐⭐⭐ | 48 个测试覆盖全面，缺 installer/scaffold 独立测试 |
| 文档质量 | ⭐⭐⭐⭐ | README 清晰，代码有 docstring |
| SKILL 质量 | ⭐⭐⭐⭐ | 本地化彻底，缺少量 Google 版精华内容 |
| 可维护性 | ⭐⭐⭐⭐ | 依赖少、代码简洁，少量硬编码需改进 |

**综合评分：8.4 / 10** — 已接近生产就绪，修复上述 S1-S3 后可发布 v0.2.1。

---

## 六、优先级修复路线图

```
P0（阻塞发布）:
  ├── S1: info --format 校验
  ├── S2: install_skills 异常捕获
  └── S3: 生成项目测试硬编码路径

P1（v0.2.1 修复）:
  ├── M1: manifest.yaml.j2 冲突清理
  ├── M2: template_version 硬编码修复
  ├── M3: Agent 检测增强
  └── M4: typecheck 目标扩展

P2（v0.3.0 优化）:
  ├── workflow SKILL 补充"代码保留原则"和"调试方法论"
  ├── 增加 langchain/llamaindex 模板支持
  ├── 添加命令速查表
  └── ruff 规则集扩展
```
