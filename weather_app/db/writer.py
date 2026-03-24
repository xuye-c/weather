# db/writer.py
from db.dbManager import dbManager

class Writer:

    @staticmethod
    def insert(city, date, temperature):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO weather (city, date, temperature) VALUES (?, ?, ?)",
            (city, date, temperature)
        )

        conn.commit()
        conn.close()


    @staticmethod
    def update(city, date, temperature):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE weather SET temperature=? WHERE city=? AND date=?",
            (temperature, city, date)
        )

        conn.commit()
        conn.close()


    @staticmethod
    def delete(city, date):
        conn = dbManager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM weather WHERE city=? AND date=?",
            (city, date)
        )

        conn.commit()
        conn.close()