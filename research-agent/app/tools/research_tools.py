import json

from langchain_core.tools import tool
from langchain_tavily import TavilySearch


def build_research_tools(
    knowledge_base_service,
    user_id: str,
    web_search_backend=None,
):
    """
    创建当前用户专属的研究工具。

    user_id 来自服务端认证上下文，
    不暴露给 LLM 作为工具参数。
    """
    tavily = web_search_backend or TavilySearch(
        max_results=5,
        topic="general",
        search_depth="basic",
        include_answer=False,
    )

    @tool("knowledge_search")
    def knowledge_search(query: str) -> str:
        """
        在当前用户的内部知识库中搜索相关资料。

        适用于检索用户上传的 PDF、TXT、
        Markdown 等内部知识文档。
        """

        documents = knowledge_base_service.search(
            query=query,
            user_id=user_id,
            k=5,
        )

        if not documents:
            return "知识库没有找到相关资料。"

        results = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            results.append({
                "rank": index,
                "content": document.page_content,
                "metadata": document.metadata,
            })

        return json.dumps(
            results,
            ensure_ascii=False,
            default=str,
        )

    @tool("web_search")
    def web_search(query: str) -> str:
        """
        使用 Tavily 搜索外部网页资料。

        适用于获取外部技术文档、
        最新信息和公开资料。
        """

        result = tavily.invoke({
            "query": query,
        })

        return json.dumps(
            result,
            ensure_ascii=False,
            default=str,
        )

    return [
        knowledge_search,
        web_search,
    ]
