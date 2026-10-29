from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["app"] == "AI Agent API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_agent_rejects_empty_question():
    response = client.post("/agent?question=%20%20")

    assert response.status_code == 400
    assert response.json()["detail"] == "Question is required"
