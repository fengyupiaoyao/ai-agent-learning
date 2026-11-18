import json
from pathlib import Path

from app.state import AgentState


class CheckpointStore:
    def __init__(
        self,
        path="checkpoint.json",
    ):
        self.path = Path(path)

    def save(
        self,
        state: AgentState,
    ):
        data = {
            "task": state.task,
            "completed_steps": state.completed_steps,
            "current_step": state.current_step,
            "status": state.status,
            "approval_required": state.approval_required,
            "approval_result": state.approval_result,
        }

        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self) -> AgentState:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return AgentState(**data)
