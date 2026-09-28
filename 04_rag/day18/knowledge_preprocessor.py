from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path

file_path = Path(__file__).resolve().parent / "data"


def load_documents():
    loader = DirectoryLoader(
        file_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )
    return text_splitter.split_documents(documents)


def main():
    documents = load_documents()
    print(f"Number of documents: {len(documents)}")
    chunks = split_documents(documents)
    print(f"Number of split documents: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"Document {i+1}:")
        print(chunk.page_content)
        print(f"Metadata: {chunk.metadata}")
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()
