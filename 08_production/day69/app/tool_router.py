from app.models import UserContext, ToolCall, ToolResult
from app.permissions import has_tool_permission
from app.tools import ToolRegistry
from app.approval import ApprovalService


class ToolRouter:
    def __init__(self):
        self.registry = ToolRegistry()
        self.approval = ApprovalService()

    def execute(
        self,
        user: UserContext,
        call: ToolCall,
        approval_id: str | None = None,
    ) -> ToolResult:
        tool = self.registry.tools.get(call.tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                error="Tool not found",
            )

        if not has_tool_permission(user, call.tool_name):
            return ToolResult(
                success=False,
                error="Permission denied",
            )

        arguments = call.arguments

        if not isinstance(arguments, dict):
            return ToolResult(
                success=False,
                error="Invalid arguments",
            )

        required = tool["required"]
        allowed = tool["allowed"]

        if not required.issubset(arguments.keys()):
            return ToolResult(
                success=False,
                error="Missing required arguments",
            )

        if not set(arguments).issubset(allowed):
            return ToolResult(
                success=False,
                error="Invalid arguments",
            )

        if tool["high_risk"]:
            if not approval_id:
                return ToolResult(
                    success=False,
                    error="Approval required",
                    requires_approval=True,
                )
            if not self.approval.is_approved(approval_id):
                return ToolResult(
                    success=False,
                    error="Approval not granted",
                    requires_approval=True,
                )

        try:
            result = tool["handler"](**arguments)

            return ToolResult(
                success=True,
                data=result,
            )
        except Exception:
            return ToolResult(
                success=False,
                error="Tool execution failed",
            )
