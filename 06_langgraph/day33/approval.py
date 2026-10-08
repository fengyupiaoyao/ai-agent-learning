from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from rich import print as pprint


class State(TypedDict):
    action: str
    approved: bool
    result: str


def approve_node(state: State):
    print("A")
    decision = interrupt({
        "type": "approve",
        "action": state["action"],
        "message": "Please approve the action",
    })

    approved = decision == "approved"

    return {"approved": approved}


def execute_node(state: State):
    if not state["approved"]:
        return {"result": "Action not approved"}

    return {"result": f"Action executed: {state['action']}"}


builder = StateGraph(State)

builder.add_node("approve", approve_node)
builder.add_node("execute", execute_node)

builder.add_edge(START, "approve")
builder.add_edge("approve", "execute")
builder.add_edge("execute", END)

checkpoint_saver = InMemorySaver()
graph = builder.compile(checkpointer=checkpoint_saver)

config = {
    "configurable": {
        "thread_id": "thread_1"
    }
}
# 第一次调用：带初始输入启动图，执行到 interrupt() 处暂停
result = graph.invoke({
    "action": "删除订单124",
    "approved": False,
    "result": ""
}, config)

pprint(result)

# 第二次调用：人工审批后恢复执行，interrupt() 返回 resume 的值
result = graph.invoke(
    Command(
        resume="approved"
    ),
    config=config
)

pprint(result)
