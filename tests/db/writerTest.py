import unittest
import os
import sys
import sqlite3

# 添加 weather_app 目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'weather_app')))

from db.dbManager import dbManager
from db.writer import Writer
from db.reader import Reader


class TestWriter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """设置测试数据库"""
        # 使用测试数据库
        cls.test_db_path = os.path.join(os.path.dirname(__file__), 'test_writer.db')
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

    # ==================== Insert Tests ====================
    
    def test_insert_success(self):
        """测试成功插入数据"""
        result = Writer.insert("Beijing", "2024-03-26", 22.5)
        
        # insert 方法没有返回值，需要查询验证
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT city, date, temperature FROM weather WHERE city=? AND date=?",
                      ("Beijing", "2024-03-26"))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Beijing")
        self.assertEqual(row[1], "2024-03-26")
        self.assertEqual(row[2], 22.5)

    def test_insert_duplicate_raises_error(self):
        """测试插入重复数据时抛出异常"""
        # 第一次插入
        Writer.insert("Shanghai", "2024-03-26", 20.3)
        
        # 第二次插入相同数据应该抛出异常
        with self.assertRaises(sqlite3.IntegrityError):
            Writer.insert("Shanghai", "2024-03-26", 25.0)

    def test_insert_multiple_records(self):
        """测试插入多条记录"""
        test_data = [
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
            ("Shanghai", "2024-03-26", 20.3),
        ]
        
        for city, date, temp in test_data:
            Writer.insert(city, date, temp)
        
        # 验证所有数据都已插入
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 3)

    def test_insert_with_negative_temperature(self):
        """测试插入负温度"""
        Writer.insert("Moscow", "2024-01-15", -15.5)
        
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("Moscow", "2024-01-15"))
        temp = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(temp, -15.5)

    def test_insert_with_zero_temperature(self):
        """测试插入零度"""
        Writer.insert("IceCity", "2024-01-15", 0.0)
        
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("IceCity", "2024-01-15"))
        temp = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(temp, 0.0)

    # ==================== Update Tests ====================
    
    def test_update_success(self):
        """测试成功更新数据"""
        # 先插入数据
        Writer.insert("Tokyo", "2024-03-26", 18.0)
        
        # 更新温度
        affected = Writer.update("Tokyo", "2024-03-26", 22.5)
        
        self.assertEqual(affected, 1)
        
        # 验证更新结果
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("Tokyo", "2024-03-26"))
        temp = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(temp, 22.5)

    def test_update_non_existent_record(self):
        """测试更新不存在的记录"""
        affected = Writer.update("NonExistent", "2024-03-26", 25.0)
        self.assertEqual(affected, 0)

    def test_update_multiple_times(self):
        """测试多次更新同一条记录"""
        Writer.insert("Paris", "2024-03-26", 15.0)
        
        Writer.update("Paris", "2024-03-26", 18.0)
        Writer.update("Paris", "2024-03-26", 20.0)
        Writer.update("Paris", "2024-03-26", 22.0)
        
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("Paris", "2024-03-26"))
        temp = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(temp, 22.0)

    def test_update_wrong_date(self):
        """测试更新错误日期的记录"""
        Writer.insert("London", "2024-03-26", 12.0)
        
        affected = Writer.update("London", "2024-03-27", 15.0)
        self.assertEqual(affected, 0)
        
        # 验证原数据未改变
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("London", "2024-03-26"))
        temp = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(temp, 12.0)

    # ==================== Delete Tests ====================
    
    def test_delete_success(self):
        """测试成功删除数据"""
        Writer.insert("Sydney", "2024-03-26", 25.0)
        
        # 验证数据存在
        self.assertTrue(Reader.exists("Sydney", "2024-03-26"))
        
        # 删除数据
        affected = Writer.delete("Sydney", "2024-03-26")
        
        self.assertEqual(affected, 1)
        
        # 验证数据已删除
        self.assertFalse(Reader.exists("Sydney", "2024-03-26"))

    def test_delete_non_existent_record(self):
        """测试删除不存在的记录"""
        affected = Writer.delete("NonExistent", "2024-03-26")
        self.assertEqual(affected, 0)

    def test_delete_twice(self):
        """测试重复删除同一条记录"""
        Writer.insert("Rome", "2024-03-26", 20.0)
        
        affected1 = Writer.delete("Rome", "2024-03-26")
        affected2 = Writer.delete("Rome", "2024-03-26")
        
        self.assertEqual(affected1, 1)
        self.assertEqual(affected2, 0)

    def test_delete_only_specific_record(self):
        """测试只删除特定记录，不影响其他"""
        Writer.insert("Berlin", "2024-03-26", 10.0)
        Writer.insert("Berlin", "2024-03-27", 12.0)
        Writer.insert("Berlin", "2024-03-28", 14.0)
        
        affected = Writer.delete("Berlin", "2024-03-27")
        self.assertEqual(affected, 1)
        
        # 验证其他记录还在
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather WHERE city='Berlin'")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 2)
        
        # 验证正确的记录被删除
        self.assertTrue(Reader.exists("Berlin", "2024-03-26"))
        self.assertFalse(Reader.exists("Berlin", "2024-03-27"))
        self.assertTrue(Reader.exists("Berlin", "2024-03-28"))

    # ==================== Integration Tests ====================
    
    def test_insert_update_delete_sequence(self):
        """测试完整的插入-更新-删除流程"""
        # Insert
        Writer.insert("Osaka", "2024-03-26", 18.0)
        self.assertTrue(Reader.exists("Osaka", "2024-03-26"))
        
        # Update
        Writer.update("Osaka", "2024-03-26", 22.0)
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("Osaka", "2024-03-26"))
        temp = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(temp, 22.0)
        
        # Delete
        Writer.delete("Osaka", "2024-03-26")
        self.assertFalse(Reader.exists("Osaka", "2024-03-26"))

    def test_multiple_cities_independent(self):
        """测试多个城市的数据互不影响"""
        cities_data = [
            ("CityA", "2024-03-26", 10.0),
            ("CityB", "2024-03-26", 20.0),
            ("CityC", "2024-03-26", 30.0),
        ]
        
        for city, date, temp in cities_data:
            Writer.insert(city, date, temp)
        
        # 更新 CityB
        Writer.update("CityB", "2024-03-26", 25.0)
        
        # 删除 CityA
        Writer.delete("CityA", "2024-03-26")
        
        # 验证结果
        self.assertFalse(Reader.exists("CityA", "2024-03-26"))
        
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("CityB", "2024-03-26"))
        temp_b = cursor.fetchone()[0]
        self.assertEqual(temp_b, 25.0)
        
        cursor.execute("SELECT temperature FROM weather WHERE city=? AND date=?",
                      ("CityC", "2024-03-26"))
        temp_c = cursor.fetchone()[0]
        self.assertEqual(temp_c, 30.0)
        conn.close()

    def test_edge_cases(self):
        """测试边界情况"""
        # 极端温度
        Writer.insert("HotCity", "2024-03-26", 60.0)
        Writer.insert("ColdCity", "2024-03-26", -225.0)
        
        # 特殊字符城市名
        Writer.insert("New York", "2024-03-26", 15.0)
        Writer.insert("São Paulo", "2024-03-26", 25.0)
        
        # 验证所有数据都存在
        self.assertTrue(Reader.exists("HotCity", "2024-03-26"))
        self.assertTrue(Reader.exists("ColdCity", "2024-03-26"))
        self.assertTrue(Reader.exists("New York", "2024-03-26"))
        self.assertTrue(Reader.exists("São Paulo", "2024-03-26"))


if __name__ == "__main__":
    unittest.main()