from app.policy import PolicyEngine
from app.approval import ApprovalManager


class SafeToolExecutor:
    def __init__(self):
        self.policy = PolicyEngine()
        self.approval = ApprovalManager()

    def execute(
        self,
        tool,
        arguments: dict,
    ):
        if self.policy.requires_approval(tool):
            approved = self.approval.request_approval(tool.name, arguments)

            if not approved:
                return {
                    "status": "rejected",
                    "tool": tool.name
                }

        result = tool.handler(**arguments)

        return {
            "status": "success",
            "tool": tool.name,
            "result": result,
        }
