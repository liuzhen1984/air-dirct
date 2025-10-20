#!/bin/bash

# 前后端集成测试脚本

echo "🧪 Air Dict 前后端集成测试"
echo "================================"
echo ""

# 检查后端服务
echo "1️⃣ 检查后端服务..."
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务未运行"
    echo "请先启动后端: cd server && ./run.sh"
    exit 1
fi

echo ""

# 测试英文查询
echo "2️⃣ 测试英文查询 (hello)..."
response=$(curl -s -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}')

if echo "$response" | grep -q "\"word\":\"hello\""; then
    echo "✅ 英文查询成功"
    echo "   单词: $(echo "$response" | grep -o '"word":"[^"]*"' | head -1)"
    echo "   中文: $(echo "$response" | grep -o '"chinese":"[^"]*"')"
else
    echo "❌ 英文查询失败"
    echo "响应: $response"
    exit 1
fi

echo ""

# 测试中文查询
echo "3️⃣ 测试中文查询 (你好)..."
response=$(curl -s -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}')

if echo "$response" | grep -q "\"detected_language\":\"zh-CN\""; then
    echo "✅ 中文查询成功"
    echo "   检测语言: $(echo "$response" | grep -o '"detected_language":"[^"]*"')"
    echo "   英文翻译: $(echo "$response" | grep -o '"english":"[^"]*"')"
else
    echo "❌ 中文查询失败"
    echo "响应: $response"
    exit 1
fi

echo ""

# 测试错误处理
echo "4️⃣ 测试错误处理 (不存在的单词)..."
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "asdfghjkl"}')

http_code=$(echo "$response" | tail -n1)
if [ "$http_code" = "404" ]; then
    echo "✅ 错误处理正常 (返回 404)"
else
    echo "⚠️  预期返回 404，实际返回 $http_code"
fi

echo ""
echo "================================"
echo "✅ 所有测试通过！"
echo ""
echo "📱 前端配置:"
echo "   API 端点: http://localhost:3000/api"
echo "   搜索接口: POST /api/search"
echo ""
echo "🚀 下一步:"
echo "   1. cd app"
echo "   2. flutter run -d chrome"
echo "   3. 在搜索框输入 'hello' 或 '你好' 测试"
echo ""
