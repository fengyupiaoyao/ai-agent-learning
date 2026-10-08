from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class State(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    query: str

    retrieved_docs: list

    tool_results: list

    final_answer: str
