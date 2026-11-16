from typing import TypedDict


class Task(TypedDict):
    id: str
    description: str
    status: str
    result: str
    error: str
    attempts: int


class PlanningState(TypedDict):
    goal: str
    tasks: list[Task]
    current_index: int
    results: list[str]
    replan_count: int
    max_replans: int
    current_result: str
    current_error: str
    status: str
    fail_task_id: str
