# db/database_manager.py

import sqlite3
import os


class dbManager:
    DB_PATH = os.getenv("DB_PATH", "data/weather.db")
    @staticmethod
    def get_connection():
        return sqlite3.connect(dbManager.DB_PATH)