import pytest

from app.database import Database
from app.memory_store import MemoryStore


@pytest.fixture
def store(tmp_path):

    db = Database(
        str(tmp_path / "memory.db")
    )

    return MemoryStore(db)


def test_add_and_get_memory(store):

    memory = store.add_memory(
        user_id="user_001",
        category="profile",
        content="用户熟悉 Python",
    )

    result = store.get_memory(
        "user_001",
        memory.memory_id,
    )

    assert result is not None
    assert result.content == "用户熟悉 Python"


def test_duplicate_memory(store):

    first = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    second = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    assert first.memory_id == second.memory_id


def test_update_memory(store):

    memory = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    updated = store.update_memory(
        "user_001",
        memory.memory_id,
        content="用户熟悉 Python 和 LangGraph",
    )

    assert updated.content == (
        "用户熟悉 Python 和 LangGraph"
    )


def test_delete_memory(store):

    memory = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    deleted = store.delete_memory(
        "user_001",
        memory.memory_id,
    )

    assert deleted is True

    result = store.get_memory(
        "user_001",
        memory.memory_id,
    )

    assert result is None


def test_user_isolation(store):

    memory = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    result = store.get_memory(
        "user_002",
        memory.memory_id,
    )

    assert result is None


def test_update_conflicting_memory(store):

    first = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Python",
    )

    second = store.add_memory(
        "user_001",
        "profile",
        "用户熟悉 Java",
    )

    with pytest.raises(ValueError):
        store.update_memory(
            "user_001",
            second.memory_id,
            content="用户熟悉 Python",
        )
