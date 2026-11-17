from typing import Literal
from pydantic import BaseModel, Field


class Finding(BaseModel):
    title: str
    content: str
    source: str


class ResearchOutput(BaseModel):
    topic: str
    findings: list[Finding]
    status: Literal["completed", "failed"]


class AnalysisOutput(BaseModel):
    topic: str
    advantages: list[str]
    disadvantages: list[str]
    conclusion: str


class ReviewOutput(BaseModel):
    approved: bool
    score: int = Field(ge=0, le=100)
    feedback: str
