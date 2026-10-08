from turtle import st
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    message: str
    human_response: str


def ask_human(state: State):
    answer = interrupt("请输入你的决定：")

    return {
        "human_response": answer
    }


builder = StateGraph(State)

builder.add_node("ask_human", ask_human)

builder.add_edge(START, "ask_human")
builder.add_edge("ask_human", END)

checkpoint_saver = InMemorySaver()

graph = builder.compile(checkpointer=checkpoint_saver)

config = {
    "configurable": {
        "thread_id": "thread_1"
    }
}

result = graph.invoke({
    "message": "你好",
    "human_response": ""
}, config)

print(result)

result = graph.invoke(
    Command(
        resume="继续",
    ),
    config
)
print(result)
