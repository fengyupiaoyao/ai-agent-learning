from app.models import UserContext

ROLE_TOOLS = {
    "viewer": {
        "search_docs",
    },
    "researcher": {
        "search_docs",
        "read_file",
    },
    "operator": {
        "search_docs",
        "read_file",
        "send_email",
    },
    "admin": {
        "search_docs",
        "read_file",
        "send_email",
        "delete_file",
    },
}


def has_tool_permission(
    user: UserContext,
    tool_name: str,
) -> bool:
    allowed_tools = ROLE_TOOLS.get(user.role, set())
    return tool_name in allowed_tools
