from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b


TOOLS = {
    "add": add,
    "multiply": multiply
}

TOOL_DESCRIPTIONS = {
    "add": {
        "description": "计算两个整数的和",
        "parameters": {
            "a": "integer",
            "b": "integer",
        },
    },

    "multiply": {
        "description": "计算两个整数的乘积",
        "parameters": {
            "a": "integer",
            "b": "integer",
        },
    },
}
