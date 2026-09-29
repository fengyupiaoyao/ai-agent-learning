from langchain_core.splitter import RecursiveCharacterTextSplitter
from data import documents

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)
split_documents = splitter.split_documents(documents)
