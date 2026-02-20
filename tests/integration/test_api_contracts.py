"""Integration tests for API error handling, middleware, and contracts."""

from __future__ import annotations

import socket
import threading
import time

import httpx
import pytest
import uvicorn

from careerdex.api.main import app

# ---------------------------------------------------------------------------
# Server fixture
# ---------------------------------------------------------------------------

def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def live_server() -> tuple[str, uvicorn.Server, threading.Thread]:
    """Start a real Uvicorn server for the module's tests."""
    port = _get_free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 5
    while not server.started and time.time() < deadline:
        time.sleep(0.05)

    if not server.started:
        server.should_exit = True
        thread.join(timeout=2)
        pytest.skip("Uvicorn server failed to start")

    yield f"http://127.0.0.1:{port}", server, thread

    server.should_exit = True
    thread.join(timeout=5)


# ---------------------------------------------------------------------------
# Middleware integration tests
# ---------------------------------------------------------------------------

class TestMiddleware:
    """Verify middleware behaviour through the real HTTP stack."""

    def test_request_id_header_present(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/")
        assert "X-Request-ID" in resp.headers
        assert len(resp.headers["X-Request-ID"]) > 0

    def test_request_id_unique_per_request(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            id1 = client.get(f"{base}/").headers["X-Request-ID"]
            id2 = client.get(f"{base}/").headers["X-Request-ID"]
        assert id1 != id2

    def test_metrics_endpoint_contains_counters(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            # Hit root first to generate a metric
            client.get(f"{base}/")
            resp = client.get(f"{base}/metrics")
        assert resp.status_code == 200
        body = resp.text
        assert "http_requests_total" in body or "HELP" in body


# ---------------------------------------------------------------------------
# Error-path integration tests
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Validate error responses conform to the ErrorResponse schema."""

    def test_404_returns_json_error(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/nonexistent-endpoint")
        assert resp.status_code == 404
        data = resp.json()
        assert "error" in data
        assert "message" in data

    def test_validation_error_on_echo(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        """POST /echo with invalid body should return 422 with details."""
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(
                f"{base}/echo",
                json={"message": "hi", "count": -1},
            )
        assert resp.status_code == 422
        data = resp.json()
        assert data["error"] == "validation_error"
        assert "details" in data
        assert len(data["details"]) > 0

    def test_validation_error_missing_fields(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(f"{base}/echo", json={})
        assert resp.status_code == 422
        data = resp.json()
        assert data["error"] == "validation_error"


# ---------------------------------------------------------------------------
# API contract tests
# ---------------------------------------------------------------------------

class TestAPIContracts:
    """Verify response shapes match documented schemas."""

    def test_root_contract(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/")
        assert resp.status_code == 200
        data = resp.json()
        assert set(data.keys()) == {"message", "version"}
        assert isinstance(data["message"], str)
        assert isinstance(data["version"], str)

    def test_health_contract(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "alive"}

    def test_startup_contract(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/startup")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] in {"started", "starting"}

    def test_readiness_contract(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/ready")
        if resp.status_code == 200:
            data = resp.json()
            assert "status" in data
            assert "components" in data
            assert isinstance(data["components"], list)
        else:
            assert resp.status_code == 503

    def test_echo_contract(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(
                f"{base}/echo",
                json={"message": "hello", "count": 3},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "hello"
        assert data["count"] == 3
        assert data["echo"] == ["hello", "hello", "hello"]

    def test_openapi_yaml_parseable(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        import yaml

        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/openapi.yaml")
        assert resp.status_code == 200
        schema = yaml.safe_load(resp.text)
        assert "openapi" in schema
        assert "paths" in schema

    def test_openapi_json_available(
        self, live_server: tuple[str, uvicorn.Server, threading.Thread]
    ) -> None:
        base, *_ = live_server
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{base}/openapi.json")
        assert resp.status_code == 200
        data = resp.json()
        assert "openapi" in data
        assert "info" in data
