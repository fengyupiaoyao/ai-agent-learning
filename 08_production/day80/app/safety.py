HIGH_RISK_TOOLS = {
    "delete_file",
    "delete_database",
    "execute_shell",
}


def check_tool_safety(tool_name: str) -> dict:
    if tool_name in HIGH_RISK_TOOLS:
        return {
            "allowed": False,
            "requires_approval": True,
            "reason": "该工具属于高风险操作",
        }

    return {
        "allowed": True,
        "requires_approval": False,
        "reason": "普通工具，可以执行",
    }
