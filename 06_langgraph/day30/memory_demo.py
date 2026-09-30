from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.messages import BaseMessage


class State(TypedDict):
    message: list[BaseMessage]


def chatbot(state: State):
    return {
        "message": state["message"]
    }


def chat(state: State):
    print("Current: ")

    for message in state["message"]:
        print(message)
    return {}


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


checkpointer = InMemorySaver()


graph = builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "12345",
    }
}
result = graph.invoke(
    {"message": "Hello, how are you?"},
    config
)

print(result)
