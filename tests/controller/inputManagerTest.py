import unittest
import os
import sys
import sqlite3

# 添加 weather_app 目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'weather_app')))

from db.dbManager import dbManager
from db.writer import Writer
from controller.inputManager import InputManager


class TestInputManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """设置测试数据库"""
        cls.test_db_path = os.path.join(os.path.dirname(__file__), 'test_inputmanager.db')
        dbManager.DB_PATH = cls.test_db_path
        
        # 创建表
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            date TEXT NOT NULL,
            temperature REAL,
            UNIQUE(city, date)
        )
        """)
        
        conn.commit()
        conn.close()

    def setUp(self):
        """每个测试前清空数据"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather")
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """测试结束后删除测试数据库"""
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    # ==================== Validate Tests ====================
    
    def test_validate_success(self):
        """测试验证成功"""
        result = InputManager.validate("Beijing", "2024-03-26", "22.5")
        
        self.assertEqual(result["city"], "Beijing")
        self.assertEqual(result["date"], "2024-03-26")
        self.assertEqual(result["temperature"], 22.5)
        self.assertNotIn("status", result)  # 成功时不返回 status

    def test_validate_empty_city(self):
        """测试空城市名"""
        result = InputManager.validate("", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("city", result["message"].lower())

    def test_validate_whitespace_city(self):
        """测试只有空格的city"""
        result = InputManager.validate("   ", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("city", result["message"].lower())

    def test_validate_invalid_date_format(self):
        """测试无效日期格式"""
        result = InputManager.validate("Beijing", "2024-13-45", "22.5")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("date", result["message"].lower())

    def test_validate_invalid_temperature_string(self):
        """测试无效温度字符串"""
        result = InputManager.validate("Beijing", "2024-03-26", "abc")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("temperature", result["message"].lower())

    def test_validate_temperature_too_high(self):
        """测试温度过高"""
        result = InputManager.validate("Beijing", "2024-03-26", "100")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("range", result["message"].lower())

    def test_validate_temperature_too_low(self):
        """测试温度过低"""
        result = InputManager.validate("Beijing", "2024-03-26", "-300")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("range", result["message"].lower())

    def test_validate_boundary_temperature_high(self):
        """测试边界温度 - 最高"""
        result = InputManager.validate("Beijing", "2024-03-26", "60")
        
        self.assertEqual(result["temperature"], 60.0)

    def test_validate_boundary_temperature_low(self):
        """测试边界温度 - 最低"""
        result = InputManager.validate("Beijing", "2024-03-26", "-225")
        
        self.assertEqual(result["temperature"], -225.0)

    def test_validate_temperature_with_decimal(self):
        """测试小数温度"""
        result = InputManager.validate("Beijing", "2024-03-26", "22.75")
        
        self.assertEqual(result["temperature"], 22.75)

    # ==================== Insert Tests ====================
    
    def test_insert_success(self):
        """测试成功插入"""
        result = InputManager.insert("Beijing", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("success", result["message"].lower())
        
        # 验证数据确实插入
        from db.reader import Reader
        self.assertTrue(Reader.exists("Beijing", "2024-03-26"))

    def test_insert_duplicate(self):
        """测试插入重复数据"""
        InputManager.insert("Shanghai", "2024-03-26", "20.3")
        result = InputManager.insert("Shanghai", "2024-03-26", "25.0")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("already", result["message"].lower())

    def test_insert_with_validation_error(self):
        """测试插入时验证失败"""
        result = InputManager.insert("", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("city", result["message"].lower())

    def test_insert_multiple_records(self):
        """测试插入多条记录"""
        InputManager.insert("Beijing", "2024-03-26", "22.5")
        InputManager.insert("Beijing", "2024-03-27", "19.0")
        InputManager.insert("Shanghai", "2024-03-26", "20.3")
        
        from db.reader import Reader
        all_data = Reader.get_all()
        self.assertEqual(len(all_data), 3)

    # ==================== Search Tests ====================
    
    def test_search_success(self):
        """测试成功搜索"""
        InputManager.insert("Beijing", "2024-03-26", "22.5")
        
        result = InputManager.search("Beijing", None, None)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["data"][0]["city"], "Beijing")

    def test_search_with_date_range(self):
        """测试日期范围搜索"""
        InputManager.insert("Beijing", "2024-03-25", "21.0")
        InputManager.insert("Beijing", "2024-03-26", "22.5")
        InputManager.insert("Beijing", "2024-03-27", "19.0")
        
        result = InputManager.search("Beijing", "2024-03-26", "2024-03-27")
        
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["date"], "2024-03-26")
        self.assertEqual(result["data"][1]["date"], "2024-03-27")

    def test_search_with_single_date(self):
        """测试单日搜索"""
        InputManager.insert("Beijing", "2024-03-26", "22.5")
        InputManager.insert("Beijing", "2024-03-27", "19.0")
        
        result = InputManager.search("Beijing", "2024-03-26", None)
        
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["data"][0]["date"], "2024-03-26")

    def test_search_no_results(self):
        """测试搜索不存在的数据"""
        result = InputManager.search("NonExistent", None, None)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 0)

    def test_search_empty_city(self):
        """测试空城市名搜索"""
        result = InputManager.search("", None, None)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("city", result["message"].lower())

    def test_search_multiple_cities(self):
        """测试多个城市的搜索互不影响"""
        InputManager.insert("Beijing", "2024-03-26", "22.5")
        InputManager.insert("Shanghai", "2024-03-26", "20.3")
        
        result = InputManager.search("Beijing", None, None)
        
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["data"][0]["city"], "Beijing")

    # ==================== Update Tests ====================
    
    def test_update_success(self):
        """测试成功更新"""
        InputManager.insert("Tokyo", "2024-03-26", "18.0")
        
        result = InputManager.update("Tokyo", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("update", result["message"].lower())
        
        # 验证数据已更新
        from db.reader import Reader
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("Tokyo", "2024-03-26"))
        temp = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(temp, 22.5)

    def test_update_non_existent(self):
        """测试更新不存在的记录"""
        result = InputManager.update("NonExistent", "2024-03-26", "22.5")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"].lower())

    def test_update_with_validation_error(self):
        """测试更新时验证失败"""
        InputManager.insert("Paris", "2024-03-26", "15.0")
        
        result = InputManager.update("Paris", "2024-03-26", "invalid_temp")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("temperature", result["message"].lower())

    # ==================== Delete Tests ====================
    
    def test_delete_success(self):
        """测试成功删除"""
        InputManager.insert("Sydney", "2024-03-26", "25.0")
        
        result = InputManager.delete("Sydney", "2024-03-26")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("delete", result["message"].lower())
        
        # 验证数据已删除
        from db.reader import Reader
        self.assertFalse(Reader.exists("Sydney", "2024-03-26"))

    def test_delete_non_existent(self):
        """测试删除不存在的记录"""
        result = InputManager.delete("NonExistent", "2024-03-26")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"].lower())

    def test_delete_twice(self):
        """测试重复删除"""
        InputManager.insert("Rome", "2024-03-26", "20.0")
        
        result1 = InputManager.delete("Rome", "2024-03-26")
        result2 = InputManager.delete("Rome", "2024-03-26")
        
        self.assertEqual(result1["status"], "success")
        self.assertEqual(result2["status"], "error")

    # ==================== Integration Tests ====================
    
    def test_full_crud_flow(self):
        """测试完整的 CRUD 流程"""
        # Create
        result1 = InputManager.insert("Osaka", "2024-03-26", "18.0")
        self.assertEqual(result1["status"], "success")
        
        # Read
        search_result = InputManager.search("Osaka", None, None)
        self.assertEqual(len(search_result["data"]), 1)
        self.assertEqual(search_result["data"][0]["temperature"], 18.0)
        
        # Update
        result2 = InputManager.update("Osaka", "2024-03-26", "22.0")
        self.assertEqual(result2["status"], "success")
        
        # Verify update
        search_result2 = InputManager.search("Osaka", None, None)
        self.assertEqual(search_result2["data"][0]["temperature"], 22.0)
        
        # Delete
        result3 = InputManager.delete("Osaka", "2024-03-26")
        self.assertEqual(result3["status"], "success")
        
        # Verify delete
        search_result3 = InputManager.search("Osaka", None, None)
        self.assertEqual(len(search_result3["data"]), 0)

    def test_validation_before_operation(self):
        """测试操作前的验证"""
        # 无效数据不应该被插入
        result = InputManager.insert("", "2024-03-26", "22.5")
        self.assertEqual(result["status"], "error")
        
        # 验证数据库没有变化
        from db.reader import Reader
        all_data = Reader.get_all()
        self.assertEqual(len(all_data), 0)


if __name__ == "__main__":
    unittest.main()