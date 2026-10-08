from typing_extensions import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.sqlite import SqliteSaver


class State(TypedDict):
    counter: int


def increment(state: State):

    return {
        "counter": state["counter"] + 1
    }


builder = StateGraph(State)

builder.add_node(
    "increment",
    increment
)

builder.add_edge(
    START,
    "increment"
)

builder.add_edge(
    "increment",
    END
)


with SqliteSaver.from_conn_string(
    "checkpoints.db"
) as checkpointer:

    graph = builder.compile(
        checkpointer=checkpointer
    )

    config = {
        "configurable": {
            "thread_id": "thread_001"
        }
    }

    result = graph.invoke(
        {
            "counter": 100
        },
        config
    )

    print(result)
