import anyio

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.mcp import MCPAdapter

import os
from dotenv import load_dotenv
load_dotenv()


async def main():
    async with MCPAdapter(
        "http://127.0.0.1:8000/mcp"
    ) as adapter:
        tools = await adapter.list_tools()

        print("发现的工具：")
        for tool in tools:
            # print(f"- {tool.name}")
            print({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.args_schema,
            })

        model = init_chat_model(
            "openai:qwen3.8-max",
            api_key=os.environ["OPENAI_API_KEY"],
            base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            temperature=0.5,
            timeout=300,
            max_tokens=25000,
        )
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "你是一个学习研究助手。"
                "回答学习笔记相关问题时，"
                "优先使用可用的搜索工具获取依据，"
                "再根据工具结果回答。"
                "不要声称执行过实际上没有执行的工具。"
            )
        )

        result = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": "帮我搜索 MCP 相关的学习笔记，并总结重点。"}
            ]
        })

        print("\n ====== Agent 最终回答 ======\n")
        print(result["messages"][-1].content)

if __name__ == "__main__":
    anyio.run(main)
