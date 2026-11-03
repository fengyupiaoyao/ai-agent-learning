from dataclasses import dataclass
from datetime import datetime


@dataclass
class Memory:
    memory_id: str
    user_id: str
    category: str
    content: str
    source: str = "conversation"
    importance: int = 50
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id is required")

        if not self.content.strip():
            raise ValueError("content cannot be empty")

        if not 0 <= self.importance <= 100:
            raise ValueError("importance must be 0-100")

        if not self.created_at:
            self.created_at = datetime.now().isoformat()

        if not self.updated_at:
            self.updated_at = self.created_at
