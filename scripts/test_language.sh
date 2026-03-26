#!/bin/bash

echo "=== Testing Language Switch ==="

# 切换到中文
echo "Switching to Chinese..."
curl -X POST http://127.0.0.1:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"lang": "zh"}'

echo -e "\n"

# 测试中文响应
echo "Testing Chinese response:"
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Shanghai"

echo -e "\n"

# 切换到英文
echo "Switching to English..."
curl -X POST http://127.0.0.1:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"lang": "en"}'

echo -e "\n"

# 测试英文响应
echo "Testing English response:"
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Shanghai"

echo -e "\n"
