
from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

import os
from dotenv import load_dotenv
load_dotenv()


# 1. 初始化模型
llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


# 2. 定义 Agent 节点
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 3. 构建图
builder = StateGraph(MessagesState)
builder.add_node("assistant", call_model)
builder.add_edge(START, "assistant")

# 4. 配置 Checkpointer
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)


# 5. 调用同一个会话
def chat(question: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = graph.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config=config,
    )

    return result["messages"][-1].content


if __name__ == "__main__":
    print("第一轮：")
    print(chat("我正在学习 LangGraph，请记住这一点。", "user-001"))

    print("\n第二轮：")
    print(chat("我正在学习什么？", "user-001"))

    print("\n新会话：")
    print(chat("我正在学习什么？", "user-002"))
