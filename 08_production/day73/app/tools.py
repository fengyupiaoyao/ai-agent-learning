from app.roles import ROLES


def search_docs(query: str) -> list[dict]:
    """Search for documents related to the query."""

    return [
        {
            "title": "LangChain",
            "content": "提供模型、工具和 Agent 应用开发抽象。",
            "source": "official_docs",
        },
        {
            "title": "LangGraph",
            "content": "用于构建有状态、可控制的 Agent 工作流。",
            "source": "official_docs",
        },
    ]


def analyze_data(findings: list[dict]) -> dict:
    """Analyze the data and return a dictionary of findings."""

    return {
        "advantages": [
            "LangChain 提供较丰富的 LLM 应用开发抽象",
            "LangGraph 适合复杂、有状态的工作流",
        ],
        "disadvantages": [
            "需要根据项目复杂度选择合适的抽象层",
        ],
        "conclusion": "简单链式应用可考虑 LangChain，复杂工作流可考虑 LangGraph。",
    }


def validate_report(analysis: dict) -> dict:
    """Validate the report and return a dictionary of findings."""

    complete = (
        bool(analysis.get("advantages"))
        and bool(analysis.get("disadvantages"))
        and bool(analysis.get("conclusion"))
    )

    return {
        "approved": complete,
        "score": 90 if complete else 40,
        "feedback": (
            "分析内容完整"
            if complete
            else "缺少优缺点或结论，需要补充"
        ),
    }


TOOL_REGISTRY = {
    "search_docs": search_docs,
    "analyze_data": analyze_data,
    "validate_report": validate_report,
}


class PermissionDenied(Exception):
    pass


def call_tool(
    role_name: str,
    tool_name: str,
    **kwargs,
):
    role = ROLES.get(role_name)

    if role is None:
        raise PermissionDenied(f"Role '{role_name}' not found")

    if tool_name not in role.allowed_tools:
        raise PermissionDenied(
            f"Tool '{tool_name}' not allowed for role '{role_name}'")

    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        raise PermissionDenied(f"Tool '{tool_name}' not found")

    return tool(**kwargs)
