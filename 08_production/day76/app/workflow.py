from app.approval import ApprovalManager
from app.state import AgentState
from app.checkpoint import CheckpointStore


STEPS = [
    "search",
    "collect_data",
    "analyze",
    "generate_report",
    "send_report",
]


class Workflow:
    def __init__(
        self,
        store=None,
        approval=None,
        interactive=False,
    ):
        self.store = store or CheckpointStore()
        self.approval = approval or ApprovalManager()
        self.interactive = interactive

    def run(
        self,
        state: AgentState,
    ):
        while state.completed_steps != STEPS:
            next_step = self.get_next_step(state)

            if next_step is None:
                break

            state.current_step = next_step

            if next_step == "send_report":
                if state.approval_result is None and self.interactive:
                    state.approval_result = self.approval.request_approval(
                        next_step,
                        {"task": state.task},
                    )

                    state.approval_required = False

                if state.approval_result is None:
                    state.status = "waiting_approval"
                    state.approval_required = True

                    self.store.save(state)

                    return state

                if not state.approval_result:
                    state.status = "rejected"

                    self.store.save(state)

                    return state

            self.execute_step(
                state,
                next_step,
            )

            state.completed_steps.append(next_step)

            self.store.save(state)

        state.status = "completed"

        self.store.save(state)

        return state

    def get_next_step(
        self,
        state: AgentState,
    ):
        for step in STEPS:
            if step not in state.completed_steps:
                return step
        return None

    def execute_step(
        self,
        state,
        step,
    ):
        print(f"Executing step: {step}")

        if step == "search":
            print("Searching information...")

        elif step == "collect_data":
            print("Collecting data...")

        elif step == "analyze":
            print("Analyzing data...")

        elif step == "generate_report":
            print("Generating report...")

        elif step == "send_report":
            print("Sending report...")
