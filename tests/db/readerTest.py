import unittest
import os
from weather_app.db.dbManager import dbManager
from weather_app.db.reader import Reader

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

    # ---------------------------
    # get_by_city
    # ---------------------------
    def test_get_by_city(self):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("Durham", "2026-03-23", 20)
        )

        conn.commit()
        conn.close()

        result = Reader.get_by_city("Durham")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Durham")

    # ---------------------------
    # exists
    # ---------------------------
    def test_exists_true(self):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            ("NYC", "2026-03-24", 10)
        )

        conn.commit()
        conn.close()

        self.assertTrue(Reader.exists("NYC", "2026-03-24"))

    def test_exists_false(self):
        self.assertFalse(Reader.exists("FakeCity", "2000-01-01"))

    # ---------------------------
    # get_by_city_and_range
    # ---------------------------
    def test_get_by_city_and_range(self):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        data = [
            ("LA", "2026-03-20", 15),
            ("LA", "2026-03-21", 16),
            ("LA", "2026-03-22", 17),
        ]

        cursor.executemany(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            data
        )

        conn.commit()
        conn.close()

        result = Reader.get_by_city_and_range("LA", "2026-03-20", "2026-03-21")

        self.assertEqual(len(result), 2)

    # ---------------------------
    # exists_range
    # ---------------------------
    def test_exists_range_partial_missing(self):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        data = [
            ("Boston", "2026-03-20", 10),
            ("Boston", "2026-03-22", 12),
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

    def test_exists_range_all_exist(self):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        data = [
            ("Chicago", "2026-03-20", 5),
            ("Chicago", "2026-03-21", 6),
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


if __name__ == "__main__":
    unittest.main()