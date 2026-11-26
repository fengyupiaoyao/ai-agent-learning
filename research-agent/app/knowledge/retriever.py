from langchain_core.documents import Document

from app.knowledge.vector_store import VectorStoreService


class KnowledgeRetriever:
    def __init__(
        self,
        vector_store: VectorStoreService,
    ):
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        user_id: str,
        k: int = 5,
        document_id: str | None = None,
    ) -> list[Document]:
        metadata_filter = {
            "user_id": user_id,
        }

        if document_id:
            metadata_filter["document_id"] = document_id

        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=metadata_filter,
        )

    def search_with_score(
        self,
        query: str,
        user_id: str,
        k: int = 5,
    ):

        metadata_filter = {
            "user_id": user_id
        }

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=metadata_filter,
        )

    def as_retriever(
        self,
        user_id: str,
        k: int = 5,
    ):

        return self.vector_store.get_retriever(
            k=k,
            filter={
                "user_id": user_id
            },
        )
