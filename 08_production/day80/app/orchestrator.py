from dataclasses import dataclass, field
from typing import Any

from app.planner import create_plan
from app.agents import AgentTeam
from app.safety import check_tool_safety
from app.approval import request_approval
from app.checkpoint import save_checkpoint

from app.checkpoint import resume_task


@dataclass
class AgentTask:
    task_id: str
    user_input: str
    plan: list[str] = field(default_factory=list)
    current_step: int = 0
    results: list[dict[str, Any]] = field(default_factory=list)
    status: str = "pending"
    error: str | None = None


@dataclass
class AgentResult:
    task_id: str
    status: str
    output: str
    steps: list[dict[str, Any]]
    requires_approval: bool = False


class AgentOrchestrator:
    def __init__(self):
        self.agent_team = AgentTeam()

    def run(
        self,
        task_id: str,
        user_input: str,
        approved: bool = False,
    ) -> dict:
        plan = create_plan(user_input)

        state = {
            "task_id": task_id,
            "user_input": user_input,
            "plan": plan,
            "current_step": 0,
            "status": "pending",
            "results": [],
        }

        print("任务计划：", plan)

        is_delete = (
            "删除" in user_input
            or "delete" in user_input.lower()
        )

        if is_delete:
            safety = check_tool_safety("delete_file")

            if safety["requires_approval"]:
                state["status"] = "waiting_approval"
                save_checkpoint(task_id, state)

                if not request_approval(
                    "delete_file",
                    approved=approved,
                ):
                    state["status"] = "rejected"
                    return state

        result = self.agent_team.run_analysis(user_input)

        state["results"].append(result)
        state["current_step"] = len(plan)
        state["status"] = "completed"

        return state


def resume(
    task_id: str,
    approved: bool,
) -> dict:
    state = resume_task(task_id)

    if not approved:
        state["status"] = "rejected"
        return state

    state["approved"] = True
    state["status"] = "completed"
    state["results"].append({
        "action": "delete_file",
        "message": "审批通过，模拟执行完成",
    })

    return state
