from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from tools import add, multiply, divide

import os
from dotenv import load_dotenv

load_dotenv()

TOOLS = [
    add,
    multiply,
    divide
]

TOOL_MAP = {
    tool.name: tool
    for tool in TOOLS
}

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

llm_with_tools = llm.bind_tools(TOOLS)


def execute_tool(tool_call):
    tool_name = tool_call["name"]
    args = tool_call["args"]

    print(f"\n[Tool Call]")
    print(f"tool = {tool_name}")
    print(f"args = {args}")

    if tool_name not in TOOL_MAP:
        return ToolMessage(
            content=f"未知工具: {tool_name}",
            tool_call_id=tool_call["id"],
            status="error",
        )

    tool = TOOL_MAP[tool_name]

    try:

        result = tool.invoke(args)

        print(f"[Tool Result] {result}")

        return ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"],
            status="success",
        )

    except Exception as e:

        print(f"[Tool Error] {e}")

        return ToolMessage(
            content=f"工具执行失败: {e}",
            tool_call_id=tool_call["id"],
            status="error",
        )


def run_agent(question: str):
    messages = [
        HumanMessage(content=question)
    ]

    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        print(f"\n[LLM]")

        if response.content:
            print(response.content)

        if not response.tool_calls:
            break
        for tool_call in response.tool_calls:
            tool_call = execute_tool(tool_call)
            messages.append(tool_call)
