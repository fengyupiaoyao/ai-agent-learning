from typing import Annotated, TypedDict

import operator

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class ResearchState2(TypedDict, total=False):
    question: str

    research_plan: list[str]
    current_step: int

    retrieved_documents: list[dict]

    research_results: list[dict]

    evidence: list[dict]

    final_answer: str

    status: str
    error: str


class ResearchState(TypedDict, total=False):

    # 用户输入
    question: str
    user_id: str
    max_steps: int

    # 研究计划
    research_plan: list[dict]
    current_step: int

    # Tool Calling 消息历史
    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]

    # 研究执行结果
    research_results: Annotated[
        list[dict],
        operator.add,
    ]

    # 执行状态
    status: str
    error: str
