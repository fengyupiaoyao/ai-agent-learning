from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
AI Agent 是一种能够利用大语言模型进行推理、
调用工具并执行任务的软件系统。

Agent 通常包含 Model、Tools、State 和 Memory。

RAG 是 Retrieval-Augmented Generation。

RAG 可以让大语言模型使用外部知识。
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
)

split_text = splitter.split_text(text)

print("Chunk 数量:", len(split_text))

for i, chunk in enumerate(split_text):
    print(f"Chunk {i+1}:")
    print(chunk)
    print("\n" + "="*50 + "\n")
