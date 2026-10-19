from pydantic import BaseModel
from typing import Literal


class MemoryItem(BaseModel):
    content: str

    category: Literal[
        "skill",
        "preference",
        "goal",
        "project",
        "fact"
    ]

    importance: str

    confidence: float
