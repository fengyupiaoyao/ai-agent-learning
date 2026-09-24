from langchain.tools import tool


@tool
def research_topic(topic: str) -> str:
    """
    Research a topic and return relevant information.
    """

    knowledge = {
        "RAG": """
        RAG stands for Retrieval-Augmented Generation.
        It retrieves external information before generating an answer.
        RAG is useful when knowledge changes frequently or comes from private data.
        """,

        "Fine-tuning": """
        Fine-tuning updates model parameters using additional training data.
        It is useful for adapting model behavior, style, or task-specific patterns.
        """,

        "AI Agent": """
        AI Agents combine language models with tools, state,
        reasoning and execution capabilities.
        """
    }
    return knowledge.get(topic, "No information found.")
