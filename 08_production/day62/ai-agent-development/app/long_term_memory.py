from langgraph.store.memory import InMemoryStore


# 开发环境使用内存 Store
store = InMemoryStore()

user_namespace = (
    "users",
    "user-001",
    "preferences",
)


def save_memory(key: str, value: dict):
    store.put(
        user_namespace,
        key,
        value,
    )


def get_memory(key: str):
    item = store.get(
        user_namespace,
        key,
    )

    if item is None:
        return None

    return item.value


def search_memories():
    items = store.search(user_namespace)

    return [
        {
            "key": item.key,
            "value": item.value,
        }
        for item in items
    ]


if __name__ == "__main__":
    save_memory(
        "coding_language",
        {"language": "Python"},
    )

    save_memory(
        "learning_goal",
        {"goal": "AI Agent Development"},
    )

    print(get_memory("coding_language"))
    print(search_memories())
