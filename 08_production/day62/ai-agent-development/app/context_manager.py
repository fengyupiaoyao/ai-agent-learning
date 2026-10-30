from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)


def trim_history(
    messages: list[BaseMessage],
    max_messages: int = 10,
) -> list[BaseMessage]:
    """
    保留 System Message 和最近的对话消息。
    这里只是简单演示，生产环境需要处理工具消息配对。
    """

    system_messages = [
        message
        for message in messages
        if isinstance(message, SystemMessage)
    ]

    conversation_messages = [
        message
        for message in messages
        if not isinstance(message, SystemMessage)
    ]

    recent_messages = conversation_messages[-max_messages:]

    return system_messages + recent_messages


if __name__ == "__main__":
    messages = [
        HumanMessage(content=f"问题 {i}")
        for i in range(20)
    ]

    result = trim_history(messages, max_messages=6)

    for message in result:
        print(message.content)
