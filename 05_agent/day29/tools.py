from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """计算两个数字的商。"""
    if b == 0:
        raise ValueError("除数不能为 0")

    return a / b
