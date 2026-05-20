import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="finance_app.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Initialization Error: {e}")

    def add_transaction(self, date, description, amount, category):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (date, description, amount, category)
                    VALUES (?, ?, ?, ?)
                ''', (date, description, amount, category))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise Exception(f"Failed to insert transaction: {e}")

    def get_all_transactions(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, date, description, amount, category FROM transactions")
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Failed to fetch transactions: {e}")
    
    def clear_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions")
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to clear transactions: {e}")
