from langchain_openai import ChatOpenAI
from tools import add, multiply

import os
from dotenv import load_dotenv
from rich import print as rprint


def execute_tool(tool_call):
    name = tool_call["name"]
    args = tool_call["args"]

    if name == "add":
        return add.invoke(args)
    elif name == "multiply":
        return multiply.invoke(args)
    else:
        raise ValueError(f"Unknown tool: {name}")


load_dotenv()

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

llm_with_tools = llm.bind_tools([add, multiply])

# response = llm_with_tools.invoke("2 + 3")
# rprint(response)

# for tool_call in response.tool_calls:
#     result = execute_tool(tool_call)
#     rprint(result)
