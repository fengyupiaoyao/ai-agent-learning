from re import S
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from app.models import Task, TaskResult
from app.scheduler import topological_sort
from app.executor import execute_tasks


class SchedulerState(TypedDict):
    tasks: list[Task]
    execution_order: list[str]
    results: list[TaskResult]


def schedule_node(state: SchedulerState):
    order = topological_sort(state["tasks"])

    return {
        "execution_order": order
    }


def execute_node(state: SchedulerState):
    results = execute_tasks(
        state["tasks"],
        state["execution_order"],
    )

    return {
        "results": results
    }


builder = StateGraph(SchedulerState)

builder.add_node("schedule", schedule_node)
builder.add_node("execute", execute_node)

builder.add_edge(START, "schedule")
builder.add_edge("schedule", "execute")
builder.add_edge("execute", END)

graph = builder.compile()
