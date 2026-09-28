from pathlib import Path

from langchain_community.document_loaders import TextLoader

file_path = Path(__file__).resolve().parent / "data" / "agent.txt"

loader = TextLoader(
    file_path,
    encoding="utf-8",
)

documents = loader.load()

print("Document 数量:", len(documents))

for doc in documents:
    print("=" * 50)
    print("Document 内容:", doc.page_content)

    print("\nMetadata:")
    print(doc.metadata)
