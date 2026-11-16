from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.state import PlanningState
from app.planner import planner_node
from app.executor import executor_node
from app.evaluator import evaluator_node
from app.replanner import replanner_node


def route_after_evaluation(state):
    if state["status"] == "failed":
        return "replanner"

    if state["current_index"] >= len(state["tasks"]):
        return END

    return "executor"


def route_after_replanning(state):
    if state["status"] == "failed":
        return END

    return "executor"


def build_graph():
    builder = StateGraph(PlanningState)

    builder.add_node("planner", planner_node)
    builder.add_node("executor", executor_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("replanner", replanner_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "executor")
    builder.add_edge("executor", "evaluator")

    builder.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "executor": "executor",
            "replanner": "replanner",
            END: END
        }
    )

    builder.add_conditional_edges(
        "replanner",
        route_after_replanning,
        {
            "executor": "executor",
            END: END
        }
    )

    return builder.compile()
