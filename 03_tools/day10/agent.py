import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from openai.types.responses.namespace_tool import ToolFunction
from tools import (
    search_python_docs,
    calcuator,
    get_user,
    is_developer,
)

load_dotenv(".env")

tools = [
    calcuator,
    search_python_docs,
    get_user,
    is_developer,
]

tool_by_name = {
    tool.name: tool
    for tool in tools
}

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

model_with_tools = model.bind_tools(tools)


def run_agent(user_input: str, max_iterations: int = 5):
    messages = [
        ("human", user_input)
    ]

    for _ in range(max_iterations):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            tool = tool_by_name[tool_name]
            if tool is None:

                result = (
                    f"Tool {tool_name} "
                    f"does not exist."
                )

            else:

                try:

                    result = tool.invoke(tool_args)

                except Exception as e:

                    result = (
                        f"Tool execution failed: {e}"
                    )

            messages.append(
                ToolMessage(
                    constent=str(result),
                    tool_call_id=tool_call_id
                )
            )
    return (
        "Agent stopped: "
        "maximum iterations reached."
    )
