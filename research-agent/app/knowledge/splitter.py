from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be non-negative")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                " ",
                "。",
                "！",
                "？",
                "；",
                "，",
                ".",
                ",",
                "",
            ],
            length_function=len,
            keep_separator=True,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        if not documents:
            return []

        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
            chunk.metadata["chunk_length"] = len(chunk.page_content)

        return chunks
