class FakeAgent:
    async def ainvoke(self, state: dict) -> dict:
        question = state["messages"][0]["content"]
        return {
            "final_answer": f"Research result: {question}"
        }
