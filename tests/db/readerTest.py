import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'weather_app')))
from db.dbManager import dbManager
from db.reader import Reader

class TestReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dbManager.DB_PATH = "data/test_weather.db"

        conn = dbManager.get_connection()
        cursor = conn.cursor()

        # 创建表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            date TEXT NOT NULL,
            temperature REAL
        )
        """)

        conn.commit()
        conn.close()

    def setUp(self):
        # 👉每个测试前清空数据
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM weather")

        conn.commit()
        conn.close()

    def tearDown(self):
        """每个测试后清理"""
        pass

    # ==================== get_all ====================
    def test_get_all_empty(self):
        """测试获取空数据库"""
        result = Reader.get_all()
        self.assertEqual(len(result), 0)

    def test_get_all_with_data(self):
        """测试获取所有数据"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        test_data = [
            ("Beijing", "2024-03-26", 22.5),
            ("Shanghai", "2024-03-26", 20.3),
            ("Beijing", "2024-03-27", 19.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            test_data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_all()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], "Beijing")
        self.assertEqual(result[0][1], "2024-03-26")
        self.assertEqual(result[0][2], 22.5)

    # ==================== get_by_city ====================
    def test_get_by_city_found(self):
        """测试获取存在的城市数据"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("Durham", "2026-03-23", 20.0)
        )
        conn.commit()
        conn.close()

        result = Reader.get_by_city("Durham")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Durham")
        self.assertEqual(result[0][1], "2026-03-23")
        self.assertEqual(result[0][2], 20.0)

    def test_get_by_city_not_found(self):
        """测试获取不存在的城市"""
        result = Reader.get_by_city("NonExistentCity")
        self.assertEqual(len(result), 0)

    def test_get_by_city_multiple_records(self):
        """测试获取有多个记录的城市"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        test_data = [
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
            ("Beijing", "2024-03-28", 18.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            test_data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city("Beijing")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], "Beijing")
        self.assertEqual(result[1][1], "2024-03-27")
        self.assertEqual(result[2][2], 18.0)

    # ==================== exists ====================
    def test_exists_true(self):
        """测试存在的记录"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("NYC", "2026-03-24", 10.0)
        )
        conn.commit()
        conn.close()

        self.assertTrue(Reader.exists("NYC", "2026-03-24"))

    def test_exists_false_wrong_city(self):
        """测试错误的城市"""
        self.assertFalse(Reader.exists("FakeCity", "2000-01-01"))

    def test_exists_false_wrong_date(self):
        """测试错误的日期"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("Tokyo", "2026-03-24", 15.0)
        )
        conn.commit()
        conn.close()
        
        self.assertFalse(Reader.exists("Tokyo", "2026-03-25"))

    # ==================== get_by_city_and_range ====================
    def test_get_by_city_and_range_full_range(self):
        """测试完整的日期范围"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("LA", "2026-03-20", 15.0),
            ("LA", "2026-03-21", 16.0),
            ("LA", "2026-03-22", 17.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()

        result = Reader.get_by_city_and_range("LA", "2026-03-20", "2026-03-21")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "2026-03-20")
        self.assertEqual(result[1][1], "2026-03-21")

    def test_get_by_city_and_range_no_match(self):
        """测试没有匹配的日期范围"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("LA", "2026-03-20", 15.0)
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city_and_range("LA", "2026-03-25", "2026-03-26")
        self.assertEqual(len(result), 0)

    # ==================== get_by_city_and_range_fixed ====================
    def test_get_by_city_and_range_fixed_only_city(self):
        """测试只提供城市，不提供日期"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
            ("Shanghai", "2024-03-26", 20.3),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city_and_range_fixed("Beijing")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "Beijing")
        self.assertEqual(result[0][1], "2024-03-26")
        self.assertEqual(result[1][2], 19.0)

    def test_get_by_city_and_range_fixed_with_both_dates(self):
        """测试提供完整日期范围"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Beijing", "2024-03-25", 21.0),
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
            ("Beijing", "2024-03-28", 18.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city_and_range_fixed("Beijing", "2024-03-26", "2024-03-27")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "2024-03-26")
        self.assertEqual(result[1][1], "2024-03-27")

    def test_get_by_city_and_range_fixed_only_start_date(self):
        """测试只提供开始日期"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Beijing", "2024-03-25", 21.0),
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city_and_range_fixed("Beijing", "2024-03-26", None)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "2024-03-26")

    def test_get_by_city_and_range_fixed_only_end_date(self):
        """测试只提供结束日期"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Beijing", "2024-03-25", 21.0),
            ("Beijing", "2024-03-26", 22.5),
            ("Beijing", "2024-03-27", 19.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.get_by_city_and_range_fixed("Beijing", None, "2024-03-26")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "2024-03-26")

    def test_get_by_city_and_range_fixed_city_not_found(self):
        """测试不存在的城市"""
        result = Reader.get_by_city_and_range_fixed("NonExistentCity")
        self.assertEqual(len(result), 0)

    # ==================== exists_range ====================
    def test_exists_range_partial_missing(self):
        """测试部分缺失的日期范围"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Boston", "2026-03-20", 10.0),
            ("Boston", "2026-03-22", 12.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.exists_range("Boston", "2026-03-20", "2026-03-22")
        
        self.assertFalse(result["all_exist"])
        self.assertIn("2026-03-21", result["missing_dates"])
        self.assertEqual(len(result["missing_dates"]), 1)
        self.assertEqual(len(result["existing_dates"]), 2)

    def test_exists_range_all_exist(self):
        """测试全部存在的日期范围"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        data = [
            ("Chicago", "2026-03-20", 5.0),
            ("Chicago", "2026-03-21", 6.0),
        ]
        
        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
        conn.close()
        
        result = Reader.exists_range("Chicago", "2026-03-20", "2026-03-21")
        
        self.assertTrue(result["all_exist"])
        self.assertEqual(len(result["missing_dates"]), 0)
        self.assertEqual(len(result["existing_dates"]), 2)

    def test_exists_range_no_data(self):
        """测试没有数据的日期范围"""
        result = Reader.exists_range("EmptyCity", "2026-03-20", "2026-03-22")
        
        self.assertFalse(result["all_exist"])
        self.assertEqual(len(result["missing_dates"]), 3)
        self.assertEqual(len(result["existing_dates"]), 0)

    def test_exists_range_single_day_exist(self):
        """测试单日存在的记录"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("Seattle", "2026-03-20", 12.0)
        )
        conn.commit()
        conn.close()
        
        result = Reader.exists_range("Seattle", "2026-03-20", "2026-03-20")
        
        self.assertTrue(result["all_exist"])
        self.assertEqual(len(result["missing_dates"]), 0)

    def test_exists_range_single_day_missing(self):
        """测试单日不存在的记录"""
        result = Reader.exists_range("Seattle", "2026-03-20", "2026-03-20")
        
        self.assertFalse(result["all_exist"])
        self.assertEqual(len(result["missing_dates"]), 1)
        self.assertEqual(result["missing_dates"][0], "2026-03-20")


if __name__ == "__main__":
    unittest.main()