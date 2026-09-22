from model import model_with_tools

from tools import (
    calculate,
    search_python_docs,
    get_user,
    get_current_time,
    search_users,
)

response = model_with_tools.invoke(
    # "帮我计算 123 * 456"
    # "查询用户 1001 的姓名"
    # "现在几点？"
    "找一个 developer 用户，名字包含 Alice"
)

for tool_call in response.tool_calls:
    if tool_call["name"] == "calculate":
        result = calculate.invoke(tool_call["args"])
        print("\nCalculator Result:")
        print(result)
    if tool_call["name"] == "get_user":
        result = get_user.invoke(tool_call["args"])
        print("\nGet User Name Result:")
        print(result)
    if tool_call["name"] == "search_python_docs":
        result = search_python_docs.invoke(tool_call["args"])
        print("\nSearch Python Docs Result:")
        print(result)
    if tool_call["name"] == "get_current_time":
        result = get_current_time.invoke(tool_call["args"])
        print("\nGet Current Time Result:")
        print(result)
    if tool_call["name"] == "search_users":
        result = search_users.invoke(tool_call["args"])
        print("\nSearch Users Result:")
        print(result)
