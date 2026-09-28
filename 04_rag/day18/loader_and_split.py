from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path

file_path = Path(__file__).resolve().parent / "data" / "rag.md"
loader = TextLoader(
    file_path,
    encoding="utf-8",
)

documents = loader.load()

print("原始文档数量:", len(documents))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

split_documents = text_splitter.split_documents(documents)

print("分块文档数量:", len(split_documents))

for i, document in enumerate(split_documents):
    print(f"Document {i+1}:")
    print(document.page_content)
    print("\n" + "="*50 + "\n")
