#!/bin/bash
export LANG=zh_CN.UTF-8
echo "=== Testing Error Messages ==="

# 测试1: 插入重复数据
echo "Test 1: Insert duplicate record..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-03-26" \
  -d "temperature=25.0"
echo -e "\n"

# 测试2: 更新不存在的记录
echo "Test 2: Update non-existent record..."
curl -X POST http://127.0.0.1:5000/api/update \
  -d "city=NonExistentCity" \
  -d "date=2024-03-26" \
  -d "temperature=25.0"
echo -e "\n"

# 测试3: 删除不存在的记录
echo "Test 3: Delete non-existent record..."
curl -X POST http://127.0.0.1:5000/api/delete \
  -d "city=NonExistentCity" \
  -d "date=2024-03-26"
echo -e "\n"

# 测试4: 搜索不存在的城市
echo "Test 4: Search non-existent city..."
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=NonExistentCity"
echo -e "\n"

# 测试5: 无效的温度值
echo "Test 5: Invalid temperature (too high)..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=TestCity" \
  -d "date=2024-03-26" \
  -d "temperature=1000"
echo -e "\n"

# 测试6: 空的 city
echo "Test 6: Empty city..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=" \
  -d "date=2024-03-26" \
  -d "temperature=25.0"
echo -e "\n"

# 测试7: 无效的日期格式
echo "Test 7: Invalid date format..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=TestCity" \
  -d "date=2024-13-45" \
  -d "temperature=25.0"
echo -e "\n"

curl -X POST http://127.0.0.1:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"lang": "zh"}'

# 测试错误（应该返回中文）
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=" \
  -d "date=2024-03-26" \
  -d "temperature=25.0"
