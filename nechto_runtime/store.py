"""
SQLiteStore: Adapter for persistent state storage using SQLite.
"""
import sqlite3
import json
from typing import Any, Optional

class SQLiteStore:
    def __init__(self, db_path: str = 'nechto_state.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_tables()

    def _init_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS state (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')

    def set(self, key: str, value: Any):
        value_json = json.dumps(value)
        with self.conn:
            self.conn.execute(
                'REPLACE INTO state (key, value) VALUES (?, ?)',
                (key, value_json)
            )

    def get(self, key: str) -> Optional[Any]:
        cur = self.conn.cursor()
        cur.execute('SELECT value FROM state WHERE key = ?', (key,))
        row = cur.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def delete(self, key: str):
        with self.conn:
            self.conn.execute('DELETE FROM state WHERE key = ?', (key,))

    def keys(self):
        cur = self.conn.cursor()
        cur.execute('SELECT key FROM state')
        return [row[0] for row in cur.fetchall()]

    def close(self):
        self.conn.close()
