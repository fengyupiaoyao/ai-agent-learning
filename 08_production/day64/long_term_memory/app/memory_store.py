from ast import Delete
import uuid
from datetime import datetime

from app.database import Database
from app.models import Memory


class MemoryStore:
    def __init__(self, database: Database):
        self.database = database

    @staticmethod
    def normalize(content: str) -> str:
        return " ".join(content.lower().split())

    @staticmethod
    def row_to_memory(row):
        if row is None:
            return None
        return Memory(
            memory_id=row["memory_id"],
            user_id=row["user_id"],
            category=row["category"],
            content=row["content"],
            source=row["source"],
            importance=row["importance"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def add_memory(
        self,
        user_id: str,
        category: str,
        content: str,
        source: str = "conversation",
        importance: int = 50,
    ):
        existing = self.find_duplicate(
            user_id,
            category,
            content,
        )
        if existing:
            return existing

        now = datetime.now().isoformat()

        memory = Memory(
            memory_id=str(uuid.uuid4()),
            user_id=user_id,
            category=category,
            content=content,
            source=source,
            importance=importance,
            created_at=now,
            updated_at=now,
        )

        with self.database.connect() as conn:
            conn.execute(
                """
                INSERT INTO memories (
                    memory_id,
                    user_id,
                    category,
                    content,
                    source,
                    importance,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                    memory.memory_id,
                    memory.user_id,
                    memory.category,
                    memory.content,
                    memory.source,
                    memory.importance,
                    memory.created_at,
                    memory.updated_at,
                ))

        return memory

    def find_duplicate(self, user_id: str, category: str, content: str):
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM memories
                WHERE user_id = ? AND category = ?
                """,
                (user_id, category),
            ).fetchall()
        target = self.normalize(content)

        for row in rows:
            if self.normalize(row["content"]) == target:
                return self.row_to_memory(row)

        return None

    def get_memory(self, user_id: str, memory_id: str):
        with self.database.connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM memories
                WHERE user_id = ? AND memory_id = ?
                """,
                (user_id, memory_id),
            ).fetchone()
        return self.row_to_memory(row)

    def update_memory(
        self,
        user_id: str,
        memory_id: str,
        category: str = None,
        content: str = None,
        importance: int = None,
    ):
        memory = self.get_memory(
            user_id, memory_id
        )
        if memory is None:
            return None

        new_content = (
            content if content is not None
            else memory.content
        )

        new_category = (
            category if category is not None
            else memory.category
        )

        new_importance = (
            importance if importance is not None
            else memory.importance
        )

        if not new_content.strip():
            raise ValueError("content cannot be empty")

        if not 0 <= new_importance <= 100:
            raise ValueError("importance must be 0-100")

        # 检查是否与另一条记忆冲突
        duplicate = self.find_duplicate(
            user_id,
            new_category,
            new_content,
        )

        if (
            duplicate is not None
            and duplicate.memory_id != memory_id
        ):
            raise ValueError(
                "Memory conflicts with an existing record"
            )

        updated_at = datetime.now().isoformat()

        with self.database.connect() as conn:

            conn.execute("""
                UPDATE memories
                SET content = ?,
                    category = ?,
                    importance = ?,
                    updated_at = ?
                WHERE user_id = ?
                AND memory_id = ?
            """, (
                new_content,
                new_category,
                new_importance,
                updated_at,
                user_id,
                memory_id,
            ))

        return self.get_memory(
            user_id,
            memory_id,
        )

    def delete_memory(
        self,
        user_id: str,
        memory_id: str,
    ):

        with self.database.connect() as conn:

            cursor = conn.execute("""
                DELETE FROM memories
                WHERE user_id = ?
                AND memory_id = ?
            """, (user_id, memory_id))

            return cursor.rowcount > 0

    def list_memories(self, user_id: str):

        with self.database.connect() as conn:

            rows = conn.execute("""
                SELECT * FROM memories
                WHERE user_id = ?
                ORDER BY importance DESC, updated_at DESC
            """, (user_id,)).fetchall()

        return [
            self.row_to_memory(row)
            for row in rows
        ]
