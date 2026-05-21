import sqlite3
import os
import hashlib

class DatabaseManager:
    def __init__(self, db_path="finance_app.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Create Users Table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )
                ''')
                # Create Transactions Table (Updated with user_id and t_type)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        t_type TEXT NOT NULL,
                        date TEXT NOT NULL,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Initialization Error: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                ''', (username, self.hash_password(password)))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise Exception("Username already exists.")
        except sqlite3.Error as e:
            raise Exception(f"Failed to register: {e}")

    def authenticate_user(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM users
                    WHERE username = ? AND password_hash = ?
                ''', (username, self.hash_password(password)))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            raise Exception(f"Authentication error: {e}")

    def add_transaction(self, user_id, t_type, date, description, amount, category):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_id, t_type, date, description, amount, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, t_type, date, description, amount, category))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise Exception(f"Failed to insert transaction: {e}")

    def get_user_transactions(self, user_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, date, description, amount, category, t_type
                    FROM transactions
                    WHERE user_id = ?
                ''', (user_id,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Failed to fetch transactions: {e}")
    
    def clear_user_data(self, user_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to clear transactions: {e}")
