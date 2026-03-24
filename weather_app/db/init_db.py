# db/init_db.py

from db.dbManager import dbManager
def init_db():
    conn = dbManager.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='weather'
    """)

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
        CREATE TABLE weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            date TEXT NOT NULL,
            temperature REAL,
            UNIQUE(city, date)
        )
        """)
        conn.commit()

    conn.close()