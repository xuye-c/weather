#!/bin/bash

echo "=== Testing DELETE ==="

# 删除记录
echo "Deleting Beijing 2024-03-26..."
curl -X POST http://127.0.0.1:5000/api/delete \
  -d "city=Beijing" \
  -d "date=2024-03-26"

echo -e "\n"

# 删除不存在的记录
echo "Deleting non-existent record (should fail):"
curl -X POST http://127.0.0.1:5000/api/delete \
  -d "city=Beijing" \
  -d "date=2024-01-01"

echo -e "\n"

# 验证删除结果
echo "Verifying deletion..."
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Beijing"

echo -e "\n"