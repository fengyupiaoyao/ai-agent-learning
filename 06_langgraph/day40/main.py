from langchain_core.messages import HumanMessage
from memory_graph import graph, Context


async def handle_message(
    user_id: str,
    thread_id: str,
    user_text: str,
):
    answer = await graph.ainvoke(
        {"messages": [HumanMessage(content=user_text)]},
        context=Context(user_id=user_id),
        config={
            "configurable": {"thread_id": thread_id}
        },
    )
    extract_and_save(user_id, conversation=f"用户：{user_text}")

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="以后解释技术时，应该采用什么方式？"
            )
        ]
    },
    context=Context(user_id="demo_user"),
    config={
        "configurable": {
            "thread_id": "conversation_001"
        }
    },
)

print(result["messages"][-1].content)
