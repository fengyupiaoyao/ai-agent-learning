from app.tools import ToolDefinition, RiskLevel


class PolicyEngine:

    def requires_approval(
        self,
        tool: ToolDefinition,
    ) -> bool:
        return tool.risk_level == RiskLevel.HIGH
