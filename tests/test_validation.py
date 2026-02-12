"""Tests for request validation and error handling."""

from fastapi.testclient import TestClient

from dataenginex.main import app

client = TestClient(app)


def test_echo_success() -> None:
    response = client.post("/echo", json={"message": "hi", "count": 2})

    assert response.status_code == 200
    assert response.json() == {"message": "hi", "count": 2, "echo": ["hi", "hi"]}
    assert "X-Request-ID" in response.headers


def test_echo_validation_error() -> None:
    response = client.post("/echo", json={"message": "", "count": 0})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"] == "validation_error"
    assert payload["message"] == "Request validation failed"
    assert payload.get("request_id")
    assert payload.get("details")
    assert "X-Request-ID" in response.headers
