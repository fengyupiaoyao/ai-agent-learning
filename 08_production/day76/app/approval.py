from app.state import AgentState


class ApprovalManager:
    def request_approval(
        self,
        tool_name: str,
        arguments: dict,
    ) -> bool:
        print("\n===== APPROVAL REQUIRED =====")
        print(f"Tool: {tool_name}")
        print(f"Arguments: {arguments}")

        answer = input("Approve? [y/N]: ")

        return answer.lower() == "y"


def approve(state: AgentState, approved: bool):
    state.approval_result = approved
    state.approval_required = False

    if approved:
        state.status = "running"
    else:
        state.status = "rejected"

    return state
