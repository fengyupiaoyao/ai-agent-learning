from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import get_research_service


class FakeResearchService:
    async def run(self, question: str) -> str:
        return f"模拟研究结果：{question}"


app.dependency_overrides[get_research_service] = (
    lambda: FakeResearchService()
)

client = TestClient(app)


def teardown_module():
    app.dependency_overrides.clear()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_agent_run():
    response = client.post(
        "/agent/run",
        json={"question": "什么是 MCP？"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "模拟研究结果：什么是 MCP？"
    }


def test_empty_question():
    response = client.post(
        "/agent/run",
        json={"question": ""},
    )

    assert response.status_code == 422
