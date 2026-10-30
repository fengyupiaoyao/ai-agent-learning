from fastapi.testclient import TestClient

from app.main import app


def test_request_has_request_id():
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.headers.get("X-Request-Id")


def test_each_request_has_unique_request_id():
    with TestClient(app) as client:
        first_response = client.get("/health/live")
        second_response = client.get("/health/live")
    assert first_response.headers.get(
        "x-Request-Id") != second_response.headers.get("x-Request-Id")


def test_metrics_endpoint_is_available():
    with TestClient(app) as client:
        client.get("/health/live")
        response = client.get("/metrics")
    assert response.status_code == 200
    assert "agent_http_requests_total" in response.text
