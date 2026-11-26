from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma

from app.knowledge.embeddings import EmbeddingService


class VectorStoreService:
    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "research_knowledge",
        embedding_service: EmbeddingService | None = None,
    ):
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_service.embeddings,
            persist_directory=persist_directory,
        )

    @staticmethod
    def _normalize_metadata(
        document: Document,
    ) -> Document:
        metadata = {
            key: value
            for key, value in document.metadata.items()
            if value is not None
        }

        return Document(
            page_content=document.page_content,
            metadata=metadata,
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> list[str]:
        if not documents:
            return []

        normalized_documents = [
            self._normalize_metadata(doc)
            for doc in documents
        ]

        ids = []

        for doc in normalized_documents:
            document_id = doc.metadata.get(
                "document_id",
                "unknown",
            )

            chunk_index = doc.metadata.get(
                "chunk_index",
                len(ids),
            )

            ids.append(
                f"{document_id}_{chunk_index}"
            )

        self.vector_store.add_documents(
            documents=normalized_documents,
            ids=ids,
        )
        return ids

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: dict | None = None,
    ) -> list[Document]:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter,
        )

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter: dict | None = None,
    ):
        if k <= 0:
            raise ValueError("k 必须大于 0")

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter,
        )

    def delete_documents(
        self,
        ids: list[str],
    ):
        if ids:
            self.vector_store.delete(ids=ids)

    def get_retriever(
        self,
        k: int = 5,
        filter: dict | None = None,
    ):

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
                "filter": filter,
            },
        )
