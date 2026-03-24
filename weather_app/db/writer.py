#db/writer.py
from db.dbManager import dbManager
import sqlite3

class Writer:
    """
    Handles all write operations to the weather database.
    """

    @staticmethod
    def insert(city, date, temperature):
        """
        Insert a new weather record.

        Args:
            city (str): Name of the city
            date (str): Date in YYYY-MM-DD format
            temperature (float): Temperature value

        Raises:
            Exception: If a record with the same (city, date) already exists
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
                (city, date, temperature)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            raise Exception("Record already exists for this city and date")

        finally:
            conn.close()


    @staticmethod
    def update(city, date, temperature):
        """
        Update temperature for an existing weather record.

        Args:
            city (str): Name of the city
            date (str): Date in YYYY-MM-DD format
            temperature (float): New temperature value

        Returns:
            int: Number of rows affected (0 if no record found)
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE weather SET temperature=? WHERE city=? AND date=?",
            (temperature, city, date)
        )

        conn.commit()
        affected = cursor.rowcount
        conn.close()

        return affected


    @staticmethod
    def delete(city, date):
        """
        Delete a weather record.

        Args:
            city (str): Name of the city
            date (str): Date in YYYY-MM-DD format

        Returns:
            int: Number of rows deleted (0 if no record found)
        """
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM weather WHERE city=? AND date=?",
            (city, date)
        )

        conn.commit()
        affected = cursor.rowcount
        conn.close()

        return affected