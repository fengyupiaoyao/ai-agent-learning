import os
from dotenv import load_dotenv
from rich.pretty import pprint

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from tools import (
    search_python_docs,
    calcuator,
    get_user,
    is_developer,
)

load_dotenv()

model = init_chat_model(
    "openai:qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

agent = create_agent(
    model=model,
    tools=[
        search_python_docs,
        calcuator,
        get_user,
        is_developer,
    ],
    system_prompt="""
你是一名 Python Developer Assistant。

你的任务是帮助用户解决 Python
开发相关问题。

规则：

1. 数学计算优先使用 calculator。
2. Python 知识问题优先使用 search_python_docs。
3. 用户信息问题使用 get_user。
4. 不要编造 Tool 返回的数据。
5. 如果 Tool 返回错误，要明确告诉用户。
6. 使用中文回答。
""",
)

# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "查询用户 1001",
#             },
#         ],
#     }
# )
# pprint(result)


def chat():
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        messages.append({"role": "user", "content": user_input})
        # response = agent.invoke(
        #     {
        #         "messages": messages,
        #     }
        # )
        # messages = response["messages"]
        # print("\n Agent:")

        # print(
        #     response["messages"][-1].content
        # )
        for chunk in agent.stream({
            "messages": messages,
        }):
            for update in chunk.values():
                new_messages = update.get("messages", [])

                # 保存本步骤新增的消息
                messages.extend(new_messages)

                # 格式化输出
                for message in new_messages:
                    message.pretty_print()


if __name__ == "__main__":
    chat()
