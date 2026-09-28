from langchain_community.document_loaders import UnstructuredMarkdownLoader
from pathlib import Path

file_path = Path(__file__).resolve().parent / "data" / "rag.md"

loader = UnstructuredMarkdownLoader(file_path)

documents = loader.load()

print("Document 数量:", len(documents))

for doc in documents:
    print("=" * 50)
    print("Document 内容:", doc.page_content)

    print("\nMetadata:")
    print(doc.metadata)
