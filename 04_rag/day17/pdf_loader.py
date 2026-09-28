from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

file_path = Path(__file__).resolve().parent / "data" / "sample2.pdf"

loader = PyPDFLoader(
    file_path
)

documents = loader.load()

print("Number of pages:", len(documents))

for i, document in enumerate(documents):
    print("=" * 50)
    print("Document:", i)

    print("\n内容：")
    print(document.page_content[:500])

    print("\n元数据：")
    print(document.metadata)
