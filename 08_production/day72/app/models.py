from typing import Literal
from pydantic import BaseModel, Field

TaskStatus = Literal[
    "pending",
    "success",
    "failed",
    "blocked",
]


class Task(BaseModel):
    task_id: str
    description: str
    depends_on: list[str] = Field(default_factory=list)


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus = "pending"
    output: str | None = None
    error: str | None = None
