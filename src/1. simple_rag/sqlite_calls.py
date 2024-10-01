import sqlite3
import json

import pandas as pd


class SQLiteCalls:
    def __init__(
            self,
            db_path="sqlite.db"
    ):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)

        # cursor = conn.cursor()
        # cursor.execute('DROP TABLE IF EXISTS chat_history')
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                embedding TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def save_message(self, role: str, message: str, embedding):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            cursor = conn.cursor()
            embedding_str = json.dumps(embedding) if not isinstance(embedding, str) else embedding

            cursor.execute("""
                INSERT INTO chat_history (role, message, embedding)
                VALUES (?, ?, ?)
            """, (role, message, embedding_str))

            conn.commit()
        finally:
            conn.close()

    def load_chat_to_dataframe(self, role=""):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            if role == "user" or role == "assistant":
                df = pd.read_sql_query('''
                    SELECT role, message, embedding, date FROM chat_history
                    WHERE role = ? 
                    ORDER BY date ASC                
                ''', conn, params=(role, ))
            else:
                df = pd.read_sql_query('''
                    SELECT * FROM chat_history
                    ORDER BY date ASC                
                ''', conn)
        finally:
            conn.close()
        return df
