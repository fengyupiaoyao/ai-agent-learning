from model import model_with_tools
from tools import calculator
from tools import get_user_name

response = model_with_tools.invoke(
    # "帮我计算 123 * 456"
    "查询用户 1001 的姓名"
)

print(response)

print(response.tool_calls)

for tool_call in response.tool_calls:
    if tool_call["name"] == "calculator":
        result = calculator.invoke(tool_call["args"])
        print("\nCalculator Result:")
        print(result)
    if tool_call["name"] == "get_user_name":
        result = get_user_name.invoke(tool_call["args"])
        print("\nGet User Name Result:")
        print(result)
