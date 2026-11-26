import pytest

from langchain_core.documents import Document

from app.knowledge.loader import (
    DocumentLoader,
    DocumentLoadError,
)

from app.knowledge.splitter import DocumentSplitter


def test_load_txt(tmp_path):

    file_path = tmp_path / "test.txt"

    file_path.write_text(
        "LangGraph 是一个 Agent 工作流框架。",
        encoding="utf-8",
    )

    loader = DocumentLoader()

    documents = loader.load(
        str(file_path),
        user_id="user_001",
    )

    assert len(documents) == 1

    assert "LangGraph" in documents[0].page_content

    assert documents[0].metadata["user_id"] == "user_001"

    assert documents[0].metadata["file_type"] == ".txt"


def test_load_markdown(tmp_path):

    file_path = tmp_path / "test.md"

    file_path.write_text(
        "# LangGraph\n\nAgent 工作流框架。",
        encoding="utf-8",
    )

    documents = DocumentLoader().load(
        str(file_path)
    )

    assert len(documents) == 1

    assert documents[0].metadata["filename"] == "test.md"


def test_file_not_found():

    loader = DocumentLoader()

    with pytest.raises(DocumentLoadError):

        loader.load("not_exists.txt")


def test_unsupported_file(tmp_path):

    file_path = tmp_path / "test.exe"

    file_path.write_text(
        "test",
        encoding="utf-8",
    )

    with pytest.raises(DocumentLoadError):

        DocumentLoader().load(str(file_path))


def test_empty_document(tmp_path):

    file_path = tmp_path / "empty.txt"

    file_path.write_text(
        "",
        encoding="utf-8",
    )

    with pytest.raises(DocumentLoadError):

        DocumentLoader().load(str(file_path))


def test_document_splitter():

    document = Document(
        page_content="LangGraph 是 Agent 工作流框架。" * 100,
        metadata={
            "document_id": "doc_001",
            "filename": "test.txt",
            "page": 1,
        },
    )

    splitter = DocumentSplitter(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = splitter.split([document])

    assert len(chunks) > 1

    assert chunks[0].metadata["document_id"] == "doc_001"

    assert chunks[0].metadata["filename"] == "test.txt"

    assert "chunk_index" in chunks[0].metadata

    assert chunks[0].metadata["chunk_length"] <= 100


def test_invalid_splitter_config():

    with pytest.raises(ValueError):

        DocumentSplitter(
            chunk_size=100,
            chunk_overlap=100,
        )
