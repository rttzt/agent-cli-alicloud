# 下一步行动

> 以下任务建议交给 Coding Agent 执行。

## 1. 替换数据源占位实现

替换 tools/xhs_search.py 占位实现，接入真实的小红书数据源（搜索 API 或第三方爬虫），配置 API Key 环境变量

## 2. 实现爆文要素拆解

在 src/agent/main.py 里加入'爆文要素拆解'的 ReAct 循环，覆盖标题/封面/钩子/标签/CTA 五要素分析

## 3. 编写评测套件

参考 eval-plan.md 编写评测数据集，放入 tests/eval/ 目录，运行 pytest tests/eval/ 验证各维度达标


