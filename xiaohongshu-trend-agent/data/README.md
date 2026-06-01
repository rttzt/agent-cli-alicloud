# 测试数据

本目录包含用于测试和演示的模拟数据。

## 文件说明

- `sample_trending_notes.json` — 小红书热门笔记模拟数据集（3 品类 x 10 条）

## 使用方式

Agent 会自动加载 `data/sample_trending_notes.json` 作为数据源。

### 替换为真实数据

将第三方平台（千瓜/新红等）导出的数据转换为相同 JSON 格式，放到此目录即可：

```bash
# 格式要求
{
  "categories": {
    "品类名": [
      {"title": "...", "likes": ..., "collects": ..., ...}
    ]
  }
}
```

## 合规声明

所有数据均为模拟生成，不包含真实用户信息。
