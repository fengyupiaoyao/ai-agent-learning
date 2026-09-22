import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv(".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)


@tool
def calculator(operation: str) -> str:
    """A simple calculator tool that can add, subtract, multiply, and divide two numbers."""
    return str(eval(operation))


tools = [
    calculator
]

tools_by_name = {
    tool.name: tool
    for tool in tools
}

model_with_tools = model.bind_tools(tools)

messages = [
    (
        "human", "帮我计算 123 * 456"
    )
]

response = model_with_tools.invoke(messages)

# 直接 append 完整的 AIMessage 对象，保留 tool_calls 信息
# 否则后续的 tool 消息会因缺少对应的 assistant tool_calls 而被接口拒绝
messages.append(response)

for tool_call in response.tool_calls:
    # tool_call 是 ToolCall（TypedDict），本质是 dict，必须用下标访问
    selected_tool = tools_by_name[tool_call["name"]]
    tool_result = selected_tool.invoke(tool_call["args"])
    messages.append(
        {
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call["id"],
        }
    )

final_response = model_with_tools.invoke(messages)

print(final_response)
print(final_response.content)
