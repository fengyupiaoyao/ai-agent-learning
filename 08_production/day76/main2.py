from pathlib import Path

from app.state import AgentState
from app.workflow import Workflow
from app.approval import approve
from app.checkpoint import CheckpointStore


# True  -> 终端里输入 y / N，整个流程一次跑完
# False -> 用代码模拟审批，演示「挂起 -> 存盘 -> 恢复」两阶段
INTERACTIVE = True

STORE_PATH = Path(__file__).resolve().parent / "checkpoint.json"


def run_interactive():
    workflow = Workflow(
        store=CheckpointStore(path=STORE_PATH),
        interactive=True,
    )

    state = AgentState(
        task="research company"
    )

    return workflow.run(state)


def run_two_phase():
    workflow = Workflow(
        store=CheckpointStore(path=STORE_PATH),
        interactive=False,
    )

    # ---------- 阶段一：跑到 send_report 前挂起并存盘 ----------
    state = AgentState(
        task="research company"
    )

    state = workflow.run(state)

    print("\n[阶段一] 状态：", state.status)
    print("[阶段一] 已完成：", state.completed_steps)

    # ---------- 阶段二：从 checkpoint 恢复，审批通过后继续 ----------
    state = workflow.store.load()

    state = approve(
        state,
        approved=True
    )

    workflow.store.save(state)

    return workflow.run(state)


state = run_interactive() if INTERACTIVE else run_two_phase()

print("\nWorkflow Status:")
print(state.status)

print("\nCompleted:")
print(state.completed_steps)

print("\nCurrent:")
print(state.current_step)
