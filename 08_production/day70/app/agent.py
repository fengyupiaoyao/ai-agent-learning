from app.faults import simulated_tool, FaultPlan

from app.resilience import resilient_call
from app.checkpoint import CheckpointStore


class ReliabilityAgent:
    def __init__(self):
        self.checkpoints = CheckpointStore()

    async def run(self, task_id, plan):
        state = self.checkpoints.load(task_id) or {
            "task_id": task_id,
            "status": "running",
            "result": None,
        }

        if state["status"] == "completed":
            return state

        self.checkpoints.save(task_id, state)

        result = await resilient_call(
            lambda: simulated_tool(plan),
            timeout=0.1,
            max_retries=2,
            fallback={"result": "Using cached research data"},
        )

        state["result"] = result
        state["status"] = (
            "completed" if result["status"] in (
                "success", "fallback") else "failed"
        )

        self.checkpoints.save(task_id, state)

        return state
