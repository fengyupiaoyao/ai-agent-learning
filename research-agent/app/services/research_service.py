from app.agents.research_graph import ResearchGraph

from app.services.knowledge_base_service import KnowledgeBaseService


class ResearchService:
    def __init__(
        self,
        knowledge_base_service=None,
    ):
        self.knowledge_base_service = (
            knowledge_base_service or KnowledgeBaseService()
        )

    def run(
        self,
        question: str,
        user_id: str,
        max_steps: int = 5,
    ) -> dict:
        research_graph = ResearchGraph(
            knowledge_base_service=(self.knowledge_base_service),
            user_id=user_id,
        )

        result = research_graph.invoke(
            question=question,
            max_steps=max_steps,
        )

        return {
            "question": question,
            "user_id": user_id,
            "plan": result["research_plan"],
            "results": result["research_results"],
            "total_steps": len(
                result["research_results"]
            ),
            "status": result.get(
                "status",
                "completed",
            ),
        }
