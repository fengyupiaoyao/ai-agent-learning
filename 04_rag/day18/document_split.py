from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


documents = [
    Document(
        page_content="""
        RAG 是 Retrieval-Augmented Generation。
        它通过检索外部知识增强大语言模型。
        RAG 常用于企业知识库问答。
        """
    )
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
)

split_documents = text_splitter.split_documents(documents)

print("Chunk 数量:", len(split_documents))

for i, chunk in enumerate(split_documents):
    print(f"Chunk {i+1}:")
    print(chunk.page_content)
    print("\n" + "="*50 + "\n")
