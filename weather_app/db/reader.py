# db/reader.py
import sqlite3
from db.dbManager import dbManager
from datetime import datetime, timedelta

class Reader:
    """
    Handles all read operations from the weather database.
    """
    # db/reader.py

    @staticmethod
    def get_all():
        """获取所有记录"""
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT city, date, temperature FROM weather ORDER BY city, date")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def get_by_city(city):
        """
        Retrieve all weather records for a given city.

        Args:
            city (str): Name of the city

        Returns:
            list: List of (city, date, temperature)
        """    
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT city, date, temperature FROM weather WHERE city=?",
            (city,)
        )

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def exists(city, date):
        """
        Check whether weather record exists in database.

        Args:
            city (str): Name of the city
            date (str): Dates to check

        Returns:
            Boolean: the record exists or not
        """    
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM weather WHERE city=? AND date=?",
            (city, date)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def get_by_city_and_range(city, start_date, end_date):
        """
        Retrieve weather records for a city within a date range.

        Args:
            city (str)
            start_date (str): YYYY-MM-DD
            end_date (str): YYYY-MM-DD

        Returns:
            list: List of (city, date, temperature)
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT city, date, temperature 
            FROM weather 
            WHERE city=? AND date BETWEEN ? AND ?
            ORDER BY date
            """,
            (city, start_date, end_date)
        )

        rows = cursor.fetchall()
        conn.close()
        return rows

    def exists_range(city, start_date, end_date):
        """
        Check whether all dates in the range exist in database,
        and return missing dates.

        Args:
            city (str)
            start_date (str): YYYY-MM-DD
            end_date (str): YYYY-MM-DD

        Returns:
            dict:
                {
                    "all_exist": bool,
                    "missing_dates": list[str],
                    "existing_dates": list[str]
                }
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT date FROM weather 
            WHERE city=? AND date BETWEEN ? AND ?
            """,
            (city, start_date, end_date)
        )

        rows = cursor.fetchall()
        conn.close()

        existing_dates = {row[0] for row in rows}
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        all_dates = []
        current = start

        while current <= end:
            all_dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        missing_dates = [d for d in all_dates if d not in existing_dates]

        return {
            "all_exist": len(missing_dates) == 0,
            "missing_dates": missing_dates,
            "existing_dates": list(existing_dates)
        }
    # db/reader.py - 在 Reader 类中添加新方法

    @staticmethod
    def get_by_city_and_range_fixed(city, start_date=None, end_date=None):
        """
    get_by_city_and_range
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute(
                "SELECT city, date, temperature FROM weather WHERE city=? AND date BETWEEN ? AND ? ORDER BY date",
                (city, start_date, end_date)
            )
        elif start_date:
            cursor.execute(
                "SELECT city, date, temperature FROM weather WHERE city=? AND date=? ORDER BY date",
                (city, start_date)
            )
        elif end_date:
            cursor.execute(
                "SELECT city, date, temperature FROM weather WHERE city=? AND date=? ORDER BY date",
                (city, end_date)
            )
        else:
            cursor.execute(
                "SELECT city, date, temperature FROM weather WHERE city=? ORDER BY date",
                (city,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        return rows