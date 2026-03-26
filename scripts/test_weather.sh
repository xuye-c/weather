#!/bin/bash

echo "=== Testing Weather API ==="

# 测试多个城市的天气
cities=("Beijing" "Shanghai" "London" "InvalidCity")

for city in "${cities[@]}"; do
    echo "Getting weather for $city:"
    curl -X POST http://127.0.0.1:5000/api/search \
      -d "city=$city"
    echo -e "\n"
done