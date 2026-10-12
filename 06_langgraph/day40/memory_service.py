from uuid import uuid4

from langchain_openai import OpenAIEmbeddings
from langgraph.store.memory import InMemoryStore

import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)

store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536,
    }
)


def save_memory(
    user_id: str,
    content: str,
    category: str = "general",
) -> str:
    memory_id = str(uuid4())
    namespace = (user_id, "memories")

    store.put(
        namespace,
        memory_id,
        {
            "content": content,
            "category": category,
        }
    )

    return memory_id


def search_memory(
    user_id: str,
    query: str,
    limit: int = 5,
) -> list[dict]:
    namespace = (user_id, "memories")

    items = store.search(
        namespace,
        query=query,
        limit=limit,
    )

    return [
        {
            "id": item.key,
            "content": item.value.get("content", ""),
            "category": item.value.get("category", ""),
        }
        for item in items
    ]


if __name__ == "__main__":
    user_id = "demo_user"

    save_memory(
        user_id,
        "我正在系统学习 LangGraph 和 AI Agent 开发。",
        "learning_goal",
    )

    save_memory(
        user_id,
        "我喜欢先看完整代码，再看原理和详细解释。",
        "response_preference",
    )

    save_memory(
        user_id,
        "我已经掌握 Python 基础。",
        "skill",
    )

    query = "应该用什么方式给我讲解一个新技术？"

    results = search_memory(user_id, query)

    print("检索结果：")
    for result in results:
        print(
            f"- {result['category']} (ID: {result['id']}, Content: {result['content']})")
