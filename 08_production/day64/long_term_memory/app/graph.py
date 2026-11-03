from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.memory_store import MemoryStore
from app.memory_retriever import MemoryRetriever


class AgentState(TypedDict):
    user_id: str
    query: str
    memories: list[str]
    response: str


def build_graph(memory_store: MemoryStore):

    retriever = MemoryRetriever(memory_store)

    def retrieve_memory(state: AgentState):

        results = retriever.retrieve(
            user_id=state["user_id"],
            query=state["query"],
            limit=5,
        )

        return {
            "memories": [
                memory.content
                for memory in results
            ]
        }

    def generate_response(state: AgentState):

        memory_context = "\n".join(
            state["memories"]
        )

        response = (
            f"用户问题：{state['query']}\n"
            f"检索到的长期记忆：\n"
            f"{memory_context}\n"
            f"基于以上信息处理用户问题。"
        )

        return {
            "response": response
        }

    builder = StateGraph(AgentState)

    builder.add_node(
        "retrieve_memory",
        retrieve_memory,
    )

    builder.add_node(
        "generate_response",
        generate_response,
    )

    builder.add_edge(
        START,
        "retrieve_memory",
    )

    builder.add_edge(
        "retrieve_memory",
        "generate_response",
    )

    builder.add_edge(
        "generate_response",
        END,
    )

    return builder.compile()
