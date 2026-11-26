import logging

from langchain_core.documents import Document

from app.knowledge.loader import DocumentLoader
from app.knowledge.splitter import DocumentSplitter


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        self.loader = DocumentLoader()

        self.splitter = DocumentSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )

    def ingest(
        self,
        file_path: str,
        user_id: str = "default",
    ) -> list[Document]:
        try:
            documents = self.loader.load(
                file_path=file_path,
                user_id=user_id,
            )

            chunks = self.splitter.split(documents)

            logger.info(
                "Document ingestion completed: "
                "documents=%s chunks=%s",
                len(documents),
                len(chunks),
            )

            return chunks
        except Exception:

            logger.exception(
                "Document ingestion failed: %s",
                file_path,
            )

            raise
