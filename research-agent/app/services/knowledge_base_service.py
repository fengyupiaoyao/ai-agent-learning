from langchain_core.documents import Document

from app.services.document_service import DocumentService
from app.knowledge.vector_store import VectorStoreService
from app.knowledge.retriever import KnowledgeRetriever


class KnowledgeBaseService:
    def __init__(
        self,
        vector_store: VectorStoreService | None = None,
    ):
        self.document_service = DocumentService()

        self.vector_store = (
            vector_store or VectorStoreService()
        )

        self.retriever = KnowledgeRetriever(
            vector_store=self.vector_store,
        )

    def ingest_file(
        self,
        file_path: str,
        user_id: str,
    ) -> dict:
        chunks = self.document_service.ingest(
            file_path=file_path,
            user_id=user_id,
        )

        ids = self.vector_store.add_documents(
            chunks,
        )

        return {
            "document_id": (
                chunks[0].metadata["document_id"]
                if chunks else None
            ),
            "chunk_count": len(chunks),
            "chunk_ids": ids,
        }

    def search(
        self,
        query: str,
        user_id: str,
        k: int = 5,
        document_id: str | None = None,
    ) -> list[Document]:
        return self.retriever.search(
            query=query,
            user_id=user_id,
            k=k,
            document_id=document_id,
        )
