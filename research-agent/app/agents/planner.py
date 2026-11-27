from typing import Literal

from pydantic import BaseModel, Field


class ResearchStep(BaseModel):
    """单个研究步骤"""

    step_id: str = Field(
        description="步骤唯一标识"
    )

    task: str = Field(
        min_length=3,
        description="需要完成的研究任务"
    )

    tool: Literal[
        "knowledge_search",
        "web_search",
    ] = Field(
        description="执行该步骤需要使用的工具"
    )

    query: str = Field(
        min_length=3,
        description="实际传递给工具的检索问题"
    )


class ResearchPlan(BaseModel):
    """完整研究计划"""

    goal: str = Field(
        description="研究目标"
    )

    steps: list[ResearchStep] = Field(
        min_length=1,
        max_length=8,
        description="按执行顺序排列的研究步骤"
    )
