from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    SystemMessage,
)
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def assistant_node(state: AgentState):
    messages = [
        SystemMessage(
            content="你是一个简洁、专业的 AI Agent 开发助手。"
        ),
        *state["messages"],
    ]

    # 为了演示记忆机制，这里用简单规则模拟模型回答。
    # 实际项目中替换为 await model.ainvoke(messages)
    latest_question = state["messages"][-1].content

    if "名字" in str(latest_question):
        answer = "我会在当前会话中记住你告诉我的信息。"
    else:
        answer = (
            f"我看到了你的问题：{latest_question}。"
            "我会结合当前会话的历史消息回答。"
        )

    from langchain_core.messages import AIMessage
    return {"messages": [AIMessage(content=answer)]}


builder = StateGraph(AgentState)

builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)

# 开发阶段使用内存 Checkpointer
checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)


def chat(question: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config,
    )

    return result["messages"][-1].content


if __name__ == "__main__":
    print(chat("我正在学习 AI Agent", "session-001"))
    print(chat("我正在学习什么？", "session-001"))

    print("--- 新会话 ---")
    print(chat("我之前正在学习什么？", "session-002"))
