from langchain_core.messages import HumanMessage

from agent import graph

config = {
    "configurable": {
        "thread_id": "12345"
    }
}
result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                # content="计算 123 + 456"
                # content="先计算 20 + 30，然后把结果乘以 5"
                content="还记得我叫什么吗"
            )
        ]
    },
    config
)

for message in result["messages"]:
    print("\n---")

    print(type(message).__name__)

    print(message.content)

    if hasattr(message, "tool_calls"):
        print(message.tool_calls)
