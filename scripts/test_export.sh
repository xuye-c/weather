#!/bin/bash

echo "=== Testing Export Functions ==="
mkdir -p ./exports
# 1. 先插入测试数据
echo "Step 1: Inserting test data..."
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-03-26" \
  -d "temperature=18.5"

curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Shanghai" \
  -d "date=2024-03-26" \
  -d "temperature=20.3"

curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-03-27" \
  -d "temperature=19.0"

echo -e "\n"

# 2. 查看支持的格式
echo "Step 2: Supported formats:"
curl -X GET "http://127.0.0.1:5000/api/export/formats"
echo -e "\n"

# 3. 测试JSON导出（所有数据）
echo "Step 3: Exporting all data to JSON..."
curl -X GET "http://127.0.0.1:5000/api/export/json" \
  -o ./exports/all_weather.json
echo "Saved to exports/all_weather.json"
cat ./exports/all_weather.json
echo -e "\n"

# 4. 测试JSON导出（指定城市）
echo "Step 4: Exporting Beijing data to JSON..."
curl -X GET "http://127.0.0.1:5000/api/export/json?city=Beijing" \
  -o ./exports/beijing_weather.json
echo "Saved to exports/beijing_weather.json"
cat ./exports/beijing_weather.json
echo -e "\n"

# 5. 测试CSV导出
echo "Step 5: Exporting to CSV..."
curl -X GET "http://127.0.0.1:5000/api/export/csv?city=Beijing" \
  -o ./exports/weather_export.csv
echo "Saved to exports/weather_export.csv"
head -5 ./exports/weather_export.csv
echo -e "\n"

# 6. 测试XML导出
echo "Step 6: Exporting to XML..."
curl -X GET "http://127.0.0.1:5000/api/export/xml" \
  -o ./exports/weather_export.xml
echo "Saved to exports/weather_export.xml"
head -10 ./exports/weather_export.xml
echo -e "\n"

# 7. 测试Markdown导出
echo "Step 7: Exporting to Markdown..."
curl -X GET "http://127.0.0.1:5000/api/export/markdown?city=Shanghai" \
  -o ./exports/weather_export.md
echo "Saved to exports/weather_export.md"
head -10 ./exports/weather_export.md
echo -e "\n"

echo "=== Export Tests Completed ==="