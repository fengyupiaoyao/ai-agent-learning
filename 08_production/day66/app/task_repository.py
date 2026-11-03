class TaskRepository:
    def __init__(self, database):
        self.conn = database.conn

    def get_by_key(self, user_id, idempotency_key):
        cursor = self.conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
              AND idempotency_key = ?
            """,
            (user_id, idempotency_key),
        )
        return cursor.fetchone()
    def create_task(self, user_id, idempotency_key, request_hash):
        cursor = self.conn.execute(
            """
            INSERT INTO tasks (user_id,
                               idempotency_key,
                               request_hash,
                               status)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                idempotency_key,
                request_hash,
                "pending",
            ),
        )
        self.conn.commit()

        return cursor.lastrowid

    def update_status(
            self,
            task_id,
            status,
            result=None,
            error=None,
    ):
        self.conn.execute(
            """
            UPDATE tasks
            SET status     = ?,
                result     = ?,
                error      = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                status,
                result,
                error,
                task_id,
            ),
        )
        self.conn.commit()

    def get_by_id(self, task_id):
        cursor = self.conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )

        return cursor.fetchone()

    def create_or_get(
            self,
            user_id,
            idempotency_key,
            request_hash,
    ):
        self.conn.execute(
            """
            INSERT
            OR IGNORE INTO tasks (
                   user_id,
                   idempotency_key,
                   request_hash,
                   status
               )
               VALUES (?, ?, ?, 'pending')
            """,
            (
                user_id,
                idempotency_key,
                request_hash,
            ),
        )
        created = self.conn.execute(
            "SELECT changes()"
        ).fetchone()[0] == 1

        self.conn.commit()

        task = self.get_by_key(user_id,idempotency_key)

        if task["request_hash"] != request_hash:
            raise ValueError("同一个 Idempotency-Key 不能用于不同请求")

        return task, created
