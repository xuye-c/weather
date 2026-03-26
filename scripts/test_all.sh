#!/bin/bash
cd scripts

echo "========================================="
echo "Running All API Tests"
echo "========================================="
echo ""

# 检查服务是否运行
echo "Checking if Flask server is running..."
if ! curl -s http://127.0.0.1:5000/api/search -d "city=test" > /dev/null; then
    echo "ERROR: Flask server not running!"
    echo "Please start it with: python app.py"
    exit 1
fi

echo "Server is running!"
echo ""

# 运行所有测试
./test_insert.sh
echo "-----------------------------------------"
./test_search.sh
echo "-----------------------------------------"
./test_update.sh
echo "-----------------------------------------"
./test_delete.sh
echo "-----------------------------------------"
./test_weather.sh
echo "-----------------------------------------"
./test_language.sh

echo "========================================="
echo "All tests completed!"
echo "========================================="