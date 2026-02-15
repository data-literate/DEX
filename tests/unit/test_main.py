"""Tests for main FastAPI application."""

from fastapi.testclient import TestClient

from dataenginex.api.main import app

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
    assert response.json() == {"status": "alive"}
    assert "X-Request-ID" in response.headers


def test_readiness() -> None:
    """Test readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "components" in data
    assert "X-Request-ID" in response.headers


def test_startup() -> None:
    """Test startup check endpoint."""
    with TestClient(app) as local_client:
        response = local_client.get("/startup")
    assert response.status_code == 200
    assert response.json() == {"status": "started"}


def test_metrics_endpoint() -> None:
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Check for some expected Prometheus metrics format
    content = response.text
    assert "# HELP" in content or "# TYPE" in content or "python_info" in content


def test_docs_endpoints() -> None:
    """Swagger UI and ReDoc should be available."""
    swagger = client.get("/docs")
    assert swagger.status_code == 200
    assert "Swagger UI" in swagger.text

    redoc = client.get("/redoc")
    assert redoc.status_code == 200
    assert "Redoc" in redoc.text or "ReDoc" in redoc.text


def test_openapi_yaml_export() -> None:
    """OpenAPI YAML export should be available."""
    response = client.get("/openapi.yaml")
    assert response.status_code == 200
    assert "openapi:" in response.text
