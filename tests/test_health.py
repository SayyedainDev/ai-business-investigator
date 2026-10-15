from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_response_has_generated_request_id():
    response = client.get("/health")

    assert "x-request-id" in response.headers


def test_request_id_is_echoed_back():
    response = client.get("/health", headers={"X-Request-ID": "my-test-123"})

    assert response.headers["x-request-id"] == "my-test-123"