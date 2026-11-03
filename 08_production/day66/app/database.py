import sqlite3

class Database:
    def __init__(self, db_path="tasks.db"):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)

        self.conn.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks
            (
                id
                INTEGER
                PRIMARY
                KEY
                AUTOINCREMENT,

                user_id
                TEXT
                NOT
                NULL,

                idempotency_key
                TEXT
                NOT
                NULL,

                request_hash
                TEXT
                NOT
                NULL,

                status
                TEXT
                NOT
                NULL,

                result
                TEXT,

                error
                TEXT,

                created_at
                TIMESTAMP
                DEFAULT
                CURRENT_TIMESTAMP,

                updated_at
                TIMESTAMP
                DEFAULT
                CURRENT_TIMESTAMP,

                UNIQUE
            (
                user_id,
                idempotency_key
            )
                )
            """
        )
        self.conn.commit()
    def close(self):
        self.conn.close()