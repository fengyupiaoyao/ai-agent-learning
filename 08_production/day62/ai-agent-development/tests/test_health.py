from fastapi.testclient import TestClient

from app.main import app


def test_liveness():
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness():
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_fails_when_not_ready():
    with TestClient(app) as client:
        app.state.ready = False
        response = client.get("/health/ready")
        app.state.ready = True

    assert response.status_code == 503
    assert response.json()["detail"]["status"] == "not_ready"
