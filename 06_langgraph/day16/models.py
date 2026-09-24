from pydantic import BaseModel, Field


class ResearchResult(BaseModel):
    topic: str = Field(
        description="The research topic"
    )

    summary: str = Field(
        description="A concise summary of the research"
    )

    key_points: list[str] = Field(
        description="Important points about the topic"
    )

    sources: list[str] = Field(
        description="Sources or references used"
    )
