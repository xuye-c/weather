#!/bin/bash

echo "=== Testing UPDATE ==="

# 更新温度
echo "Updating Beijing temperature..."
curl -X POST http://127.0.0.1:5000/api/update \
  -d "city=Beijing" \
  -d "date=2024-03-26" \
  -d "temperature=22.5"

echo -e "\n"

# 更新不存在的记录
echo "Updating non-existent record (should fail):"
curl -X POST http://127.0.0.1:5000/api/update \
  -d "city=Beijing" \
  -d "date=2024-01-01" \
  -d "temperature=10.0"

echo -e "\n"