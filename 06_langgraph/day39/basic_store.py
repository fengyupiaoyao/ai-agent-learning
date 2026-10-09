from os import name
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

namespace = ("user_001", "memories")

store.put(
    namespace,
    "profile",
    {
        "name": "John Doe",
        "age": 30
    }
)

item = store.get(namespace, "profile")
print("用户资料：", item.value if item else None)

store.put(
    namespace,
    "profile",
    {
        "name": "John Doe",
        "age": 32
    }
)

item = store.get(namespace, "profile")
print("更新后：", item.value if item else None)

items = store.search(namespace, limit=10)
for item in items:
    print(item.key, item.value)

store.delete(namespace, "profile")
print("删除后：", store.get(namespace, "profile"))
