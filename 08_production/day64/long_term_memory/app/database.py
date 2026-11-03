import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = db_path

        Path(db_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.init_db()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT,
                    importance INTEGER DEFAULT 50,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """
                         )
            conn.execute("""
                CREATE INDEX IF NOT EXISTS
                idx_memories_user
                ON memories(user_id)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS
                idx_memories_category
                ON memories(user_id, category)
            """)
