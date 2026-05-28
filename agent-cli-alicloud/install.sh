#!/bin/bash
# agent-cli-alicloud 本地安装脚本
# 用法: git clone ... && cd agent-cli-alicloud && ./install.sh

set -e

echo "正在安装 agent-cli-alicloud..."

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "错误: 未找到 uv，建议：运行 'curl -LsSf https://astral.sh/uv/install.sh | sh' 安装"
    exit 1
fi

# 安装依赖
uv sync

# 运行 setup
uv run agent-cli setup

echo ""
echo "✓ 安装完成！"
echo ""
echo "下一步: 打开你的 coding agent，告诉它你的想法，例如："
echo '  "我想做一个小红书爆文分析 Agent，请用 agent-cli-alicloud"'
