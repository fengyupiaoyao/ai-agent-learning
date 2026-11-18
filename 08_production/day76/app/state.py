from dataclasses import dataclass, field
from tkinter import NO


@dataclass
class AgentState:
    task: str

    completed_steps: list[str] = field(default_factory=list)

    current_step: str | None = None

    status: str = "running"

    approval_required: bool = False

    approval_result: bool | None = None
