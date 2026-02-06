"""Tests for main FastAPI application."""

from fastapi.testclient import TestClient

from dataenginex.main import app

client = TestClient(app)


def test_root() -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "DataEngineX API"
    assert "version" in data
    assert data["version"] == app.version
    # Verify request ID is added by middleware
    assert "X-Request-ID" in response.headers


def test_health() -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    assert "X-Request-ID" in response.headers


def test_readiness() -> None:
    """Test readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
    assert "X-Request-ID" in response.headers


def test_metrics_endpoint() -> None:
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Check for some expected Prometheus metrics format
    content = response.text
    assert "# HELP" in content or "# TYPE" in content or "python_info" in content
