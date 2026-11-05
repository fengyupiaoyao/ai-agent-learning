from pydantic import BaseModel, Field, ConfigDict


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    user_id: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )


class RetrievedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str = Field(
        min_length=1,
        max_length=10000,
    )

    source: str = Field(
        min_length=1,
        max_length=300,
    )
