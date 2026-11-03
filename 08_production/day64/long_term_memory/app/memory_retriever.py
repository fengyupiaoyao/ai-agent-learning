from app.memory_store import MemoryStore


class MemoryRetriever:
    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store

    def retrieve(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
    ):
        if limit <= 0:
            raise ValueError("Limit must be greater than 0")

        memories = self.memory_store.list_memories(
            user_id
        )

        query_terms = set(
            query.lower().split()
        )

        scored = []

        for memory in memories:
            content_terms = set(
                memory.content.lower().split()
            )

            overlap = len(
                query_terms & content_terms
            )

            if overlap == 0:
                continue

            score = (
                overlap * 10 + memory.importance * 0.1
            )
            scored.append((score, memory))

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            memory
            for score, memory in scored[:limit]
        ]
