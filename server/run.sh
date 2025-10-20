#!/bin/bash

# Air Dict Python 后端启动脚本 (使用 uv)

echo "🚀 Starting Air Dict Python Server with uv..."

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
fi

# 同步依赖（uv 会自动创建虚拟环境）
echo "📚 Syncing dependencies with uv..."
uv sync

# 启动服务
echo "🎉 Starting server..."
uv run uvicorn main:app --host 0.0.0.0 --port 3000 --reload
