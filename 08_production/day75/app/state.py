from typing import Annotated, TypedDict
import operator


class ResearchItem(TypedDict):
    topic: str
    key: str
    value: str
    source: str
    confidence: float


class State(TypedDict):
    goal: str
    topics: list[str]

    topic: str

    results: Annotated[list[ResearchItem], operator.add]

    merged: dict
