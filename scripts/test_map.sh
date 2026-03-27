#!/bin/bash

echo "=== Testing Google Maps API ==="
echo ""

# 测试1: 通过 GET 请求获取北京地图链接
echo "Test 1: Get map link for Beijing (GET method)..."
curl -X GET "http://127.0.0.1:5000/api/map/Beijing"
echo -e "\n"

# 测试2: 通过 GET 请求获取上海地图链接
echo "Test 2: Get map link for Shanghai (GET method)..."
curl -X GET "http://127.0.0.1:5000/api/map/Shanghai"
echo -e "\n"

# 测试3: 通过 POST 请求获取地图链接
echo "Test 3: Get map link via POST method..."
curl -X POST http://127.0.0.1:5000/api/map \
  -d "city=Tokyo"
echo -e "\n"

# 测试4: 测试带有空格的城市名
echo "Test 4: Get map link for city with spaces (New York)..."
curl -X GET "http://127.0.0.1:5000/api/map/New%20York"
echo -e "\n"

# 测试5: 测试带有特殊字符的城市名
echo "Test 5: Get map link for city with special characters (São Paulo)..."
curl -X GET "http://127.0.0.1:5000/api/map/São%20Paulo"
echo -e "\n"

# 测试6: 测试空城市名（应该返回错误）
echo "Test 6: Get map link for empty city (should fail)..."
curl -X GET "http://127.0.0.1:5000/api/map/"
echo -e "\n"

# 测试7: 测试城市名只有空格
echo "Test 7: Get map link for whitespace city (should fail)..."
curl -X POST http://127.0.0.1:5000/api/map \
  -d "city=   "
echo -e "\n"

echo "=== Google Maps API Tests Completed ==="