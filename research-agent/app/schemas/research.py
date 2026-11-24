from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ResearchStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=5,
        max_length=2000,
        description="用户的研究问题",
    )

    max_steps: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    use_knowledge_base: bool = True

    use_web_search: bool = True


class ResearchResponse(BaseModel):
    task_id: str

    status: ResearchStatus

    question: str

    created_at: datetime


class ResearchResult(BaseModel):
    task_id: str

    status: ResearchStatus

    answer: Optional[str] = None

    sources: list[str] = Field(default_factory=list)

    error: Optional[str] = None

    completed_at: Optional[datetime] = None
