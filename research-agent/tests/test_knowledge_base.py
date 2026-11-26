import pytest

from pathlib import Path

from langchain_core.embeddings import FakeEmbeddings
from langchain_core.documents import Document

from app.knowledge.vector_store import VectorStoreService
from app.knowledge.retriever import KnowledgeRetriever


class FakeEmbeddingService:

    def __init__(self):
        self.embeddings = FakeEmbeddings(size=32)


@pytest.fixture
def vector_store(tmp_path):

    return VectorStoreService(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="test_knowledge",
        embedding_service=FakeEmbeddingService(),
    )


def test_add_documents(vector_store):

    documents = [
        Document(
            page_content="LangGraph 是 Agent 工作流框架。",
            metadata={
                "document_id": "doc_001",
                "chunk_index": 0,
                "user_id": "user_001",
            },
        )
    ]

    ids = vector_store.add_documents(documents)

    assert len(ids) == 1
    assert ids[0] == "doc_001_0"


def test_metadata_filter(vector_store):

    documents = [
        Document(
            page_content="LangGraph 使用 StateGraph。",
            metadata={
                "document_id": "doc_001",
                "chunk_index": 0,
                "user_id": "user_001",
            },
        ),
        Document(
            page_content="FastAPI 用于构建 API。",
            metadata={
                "document_id": "doc_002",
                "chunk_index": 0,
                "user_id": "user_002",
            },
        ),
    ]

    vector_store.add_documents(documents)

    results = vector_store.similarity_search(
        query="Agent 工作流",
        k=10,
        filter={
            "user_id": "user_001"
        },
    )

    assert len(results) == 1

    assert results[0].metadata["user_id"] == "user_001"


def test_search_with_score(vector_store):

    documents = [
        Document(
            page_content="Checkpoint 保存工作流状态。",
            metadata={
                "document_id": "doc_001",
                "chunk_index": 0,
                "user_id": "user_001",
            },
        )
    ]

    vector_store.add_documents(documents)

    results = vector_store.similarity_search_with_score(
        query="如何保存状态",
        k=1,
    )

    assert len(results) == 1

    document, score = results[0]

    assert isinstance(document, Document)
    assert isinstance(score, float)


def test_invalid_k(vector_store):

    with pytest.raises(ValueError):

        vector_store.similarity_search(
            query="LangGraph",
            k=0,
        )


def test_empty_documents(vector_store):

    ids = vector_store.add_documents([])

    assert ids == []


def test_delete_documents(vector_store):

    documents = [
        Document(
            page_content="测试删除文档。",
            metadata={
                "document_id": "doc_001",
                "chunk_index": 0,
                "user_id": "user_001",
            },
        )
    ]

    ids = vector_store.add_documents(documents)

    vector_store.delete_documents(ids)

    results = vector_store.similarity_search(
        query="测试删除",
        k=5,
    )

    assert results == []


def test_retriever_user_filter(vector_store):

    documents = [
        Document(
            page_content="LangGraph Agent。",
            metadata={
                "document_id": "doc_001",
                "chunk_index": 0,
                "user_id": "user_001",
            },
        ),
        Document(
            page_content="FastAPI 服务。",
            metadata={
                "document_id": "doc_002",
                "chunk_index": 0,
                "user_id": "user_002",
            },
        ),
    ]

    vector_store.add_documents(documents)

    retriever = KnowledgeRetriever(vector_store)

    results = retriever.search(
        query="技术文档",
        user_id="user_001",
        k=10,
    )

    assert len(results) == 1

    assert results[0].metadata["user_id"] == "user_001"
