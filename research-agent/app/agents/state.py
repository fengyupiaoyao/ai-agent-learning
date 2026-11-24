from typing import TypedDict


class ResearchState(TypedDict, total=False):
    question: str

    research_plan: list[str]
    current_step: int

    retrieved_documents: list[dict]

    research_results: list[dict]

    evidence: list[dict]

    final_answer: str

    status: str
    error: str
