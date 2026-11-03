from app.memory_retriever import MemoryRetriever
from app.database import Database
from app.memory_store import MemoryStore


def test_retrieve_memory(tmp_path):

    database = Database(
        str(tmp_path / "memory.db")
    )

    store = MemoryStore(database)

    store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
        importance=90,
    )

    store.add_memory(
        "user_001",
        "project",
        "正在开发 Research Agent",
        importance=95,
    )

    retriever = MemoryRetriever(store)

    results = retriever.retrieve(
        user_id="user_001",
        query="Python 开发",
        limit=5,
    )

    assert len(results) >= 1

    assert any(
        "Python" in item.content
        for item in results
    )


def test_retrieve_respects_user_isolation(tmp_path):

    database = Database(
        str(tmp_path / "memory.db")
    )

    store = MemoryStore(database)

    store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    retriever = MemoryRetriever(store)

    results = retriever.retrieve(
        user_id="user_002",
        query="Python",
    )

    assert results == []
