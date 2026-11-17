from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

HandoffStatus = Literal[
    "pending",
    "accepted",
    "rejected",
]


class HandoffEnvelope(BaseModel):
    handoff_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    task_id: str

    from_agent: str
    to_agent: str

    payload: dict

    context_summary: str = ""

    artifacts: list[str] = Field(
        default_factory=list
    )

    status: HandoffStatus = "pending"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ResearchResult(BaseModel):
    topic: str
    findings: list[dict]
    conclusion: str


class AnalysisResult(BaseModel):
    topic: str
    advantages: list[str]
    disadvantages: list[str]
    conclusion: str


class ReviewResult(BaseModel):
    approved: bool
    score: int = Field(ge=0, le=100)
    feedback: str
