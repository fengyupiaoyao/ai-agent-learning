from langgraph.store.memory import InMemoryStore

store = InMemoryStore()


def save_user_preferences(user_id: str, preference: dict):
    store.put(
        ("users", user_id),
        "preferences",
        preference
    )


def get_user_preferences(user_id: str):
    return store.get(
        ("users", user_id),
        "preferences"
    )
