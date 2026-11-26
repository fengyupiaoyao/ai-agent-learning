from cgi import test
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

import os
load_dotenv()


class EmbeddingService:
    def __init__(
        self,
        model: str = "text-embedding-v3",
    ):
        self.model = model

        self.embeddings = OpenAIEmbeddings(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
        )

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        return self.embeddings.embed_documents(texts)
