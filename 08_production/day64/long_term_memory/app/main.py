from app.database import Database
from app.memory_store import MemoryStore
from app.memory_retriever import MemoryRetriever


def main():
    database = Database()

    store = MemoryStore(database)

    retriever = MemoryRetriever(store)

    user_id = "user_001"

    memory1 = store.add_memory(
        user_id=user_id,
        category="profile",
        content="用户熟悉 Python",
        importance=90,
    )

    memory2 = store.add_memory(
        user_id=user_id,
        category="preference",
        content="用户喜欢代码示例",
        importance=85,
    )

    memory3 = store.add_memory(
        user_id=user_id,
        category="project",
        content="正在开发 Research Agent",
        importance=95,
    )

    for memory in [memory1, memory2, memory3]:
        print(memory)

    results = retriever.retrieve(
        user_id=user_id,
        query="Python 开发",
        limit=5,
    )

    for memory in results:
        print(memory.content)

    updated = store.update_memory(
        user_id=user_id,
        memory_id=memory1.memory_id,
        content="用户熟悉 Python 和 LangGraph",
        importance=95,
    )

    print(updated)

    # 4. 查看所有记忆
    print("\n=== 当前全部记忆 ===")

    for memory in store.list_memories(user_id):
        print(
            memory.category,
            memory.content,
            memory.importance,
        )


if __name__ == "__main__":
    main()
