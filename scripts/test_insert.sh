#!/bin/bash

echo "=== Testing INSERT ==="

# 插入北京数据
echo "Inserting Beijing..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-03-26" \
  -d "temperature=18.5"

echo -e "\n"

# 插入上海数据
echo "Inserting Shanghai..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Shanghai" \
  -d "date=2024-03-26" \
  -d "temperature=20.3"

echo -e "\n"

# 插入重复数据（测试错误处理）
echo "Inserting duplicate (should fail)..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-03-26" \
  -d "temperature=22.0"

echo -e "\n"