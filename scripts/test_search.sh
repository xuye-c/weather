#!/bin/bash

echo "=== Testing SEARCH ==="

# 搜索所有北京数据
echo "Search all Beijing:"
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Beijing"

echo -e "\n"

# 搜索日期范围
echo "Search Beijing (2024-03-01 to 2024-03-31):"
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Beijing" \
  -d "start_date=2024-03-01" \
  -d "end_date=2024-03-31"

echo -e "\n"

# 搜索不存在的城市
echo "Search non-existent city:"
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=NonExistentCity"

echo -e "\n"