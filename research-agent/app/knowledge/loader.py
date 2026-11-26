import logging
import uuid

from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".markdown",
}

MAX_FILE_SIZE = 20 * 1024 * 1024


class DocumentLoadError(Exception):
    """文档加载异常"""


class DocumentLoader:
    def load(
        self,
        file_path: str,
        user_id: str = "default",
    ) -> list[Document]:
        path = Path(file_path)

        if not path.exists() or not path.is_file():
            raise DocumentLoadError(
                f"文件 {file_path} 不存在或不是文件"
            )

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise DocumentLoadError(
                f"文件 {file_path} 不支持的文件类型"
            )

        if path.stat().st_size > MAX_FILE_SIZE:
            raise DocumentLoadError(
                f"文件 {file_path} 太大，最大支持 {MAX_FILE_SIZE} 字节"
            )

        document_id = str(uuid.uuid4())

        uploaded_at = datetime.now(
            timezone.utc
        ).isoformat()

        base_metadata = {
            "document_id": document_id,
            "filename": path.name,
            "file_type": path.suffix.lower(),
            "source": path.name,
            "uploaded_at": uploaded_at,
            "user_id": user_id,
        }

        try:
            if path.suffix.lower() == ".pdf":
                documents = self._load_pdf(
                    path,
                    base_metadata,
                )
            else:
                documents = self._load_text(
                    path,
                    base_metadata,
                )
            if not documents:
                raise DocumentLoadError(
                    f"文件 {file_path} 没有内容"
                )
            logger.info(
                "Document loaded: filename=%s count=%s",
                path.name,
                len(documents),
            )

            return documents
        except DocumentLoadError:
            raise

        except Exception as exc:

            logger.exception(
                "Document parsing failed: %s",
                path.name,
            )

            raise DocumentLoadError(
                f"文档解析失败: {path.name}"
            ) from exc

    def _load_pdf(
        self,
        path: Path,
        metadata: dict,
    ) -> list[Document]:
        reader = PdfReader(path)

        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            page_metadata = {
                **metadata,
                "page": page_number,
            }

            documents.append(
                Document(
                    page_content=text,
                    metadata=page_metadata,
                )
            )
        return documents

    def _load_text(
        self,
        path: Path,
        metadata: dict,
    ) -> list[Document]:
        text = path.read_text(
            encoding="utf-8",
        )

        if not text.strip():
            return []

        return [
            Document(
                page_content=text,
                metadata={
                    **metadata,
                    "page": None,
                }
            )
        ]
