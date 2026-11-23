import json
from pathlib import Path
from uu import encode

CHECKPOINT_DIR = Path("checkpoints")
CHECKPOINT_DIR.mkdir(exist_ok=True)


def save_checkpoint(task_id: str, state: dict):
    path = CHECKPOINT_DIR / f"{task_id}.json"

    path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_checkpoint(task_id: str) -> dict | None:
    path = CHECKPOINT_DIR / f"{task_id}.json"

    if not path.exists():
        return None

    return json.loads(path.read_text(encoding="utf-8"))


def resume_task(task_id: str) -> dict:
    state = load_checkpoint(task_id)

    if state is None:
        raise ValueError(f"Checkpoint 不存在：{task_id}")

    if state["status"] != "waiting_approval":
        raise ValueError("当前任务不是等待审批状态")

    return state
