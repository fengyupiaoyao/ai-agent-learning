from tools import add, multiply, divide

TOOLS = {
    "add": add,
    "multiply": multiply,
    "divide": divide,
}


def execute_tool(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]
    try:
        result = tool.invoke(tool_args)
        return {
            "status": "success",
            "output": result
        }
    except Exception as e:
        return {
            "status": "error",
            "output": str(e)
        }


result = execute_tool({
    "name": "divide",
    "args": {
        "a": 1,
        "b": 0
    }
})
print(result)
