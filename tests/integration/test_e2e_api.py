"""End-to-end API tests using a real Uvicorn server."""

from __future__ import annotations

import socket
import threading
import time

import httpx
import pytest
import uvicorn

from careerdex.api.main import app


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _run_server(port: int) -> tuple[uvicorn.Server, threading.Thread]:
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to start
    deadline = time.time() + 5
    while not server.started and time.time() < deadline:
        time.sleep(0.05)

    if not server.started:
        server.should_exit = True
        thread.join(timeout=2)
        pytest.skip("Uvicorn server failed to start in time")

    return server, thread


def _stop_server(server: uvicorn.Server, thread: threading.Thread) -> None:
    server.should_exit = True
    thread.join(timeout=5)


def test_e2e_root_health_ready() -> None:
    """Spin up Uvicorn and validate core endpoints."""
    port = _get_free_port()
    server, thread = _run_server(port)

    try:
        base_url = f"http://127.0.0.1:{port}"
        with httpx.Client(timeout=5.0) as client:
            root = client.get(f"{base_url}/")
            assert root.status_code == 200
            assert root.json().get("message") == "CareerDEX API"

            health = client.get(f"{base_url}/health")
            assert health.status_code == 200
            assert health.json() == {"status": "alive"}

            ready = client.get(f"{base_url}/ready")
            assert ready.status_code in {200, 503}
            payload = ready.json()
            if ready.status_code == 200:
                assert "status" in payload
            else:
                assert payload["error"] == "service_unavailable"
    finally:
        _stop_server(server, thread)
