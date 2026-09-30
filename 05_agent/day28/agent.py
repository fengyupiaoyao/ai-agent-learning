from langchain_core.messages import HumanMessage, ToolMessage
from llm import llm_with_tools, execute_tool
from rich import print as rprint


messages = [
    HumanMessage(content="计算 123 + 456 ?")
]

while True:
    response = llm_with_tools.invoke(messages)

    rprint(response)
    messages.append(response)

    if not response.tool_calls:
        break

    for tool_call in response.tool_calls:
        result = execute_tool(tool_call)
        messages.append(
            ToolMessage(content=result, tool_call_id=tool_call["id"])
        )
print(response.content)
