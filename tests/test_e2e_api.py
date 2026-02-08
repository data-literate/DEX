"""End-to-end API tests using a real Uvicorn server."""

from __future__ import annotations

import socket
import threading
import time

import httpx
import uvicorn

from dataenginex.main import app


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _run_server(port: int) -> uvicorn.Server:
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to start
    timeout = time.time() + 5
    while not server.started and time.time() < timeout:
        time.sleep(0.05)

    return server


def _stop_server(server: uvicorn.Server) -> None:
    server.should_exit = True


def test_e2e_root_health_ready() -> None:
    """Spin up Uvicorn and validate core endpoints."""
    port = _get_free_port()
    server = _run_server(port)

    try:
        base_url = f"http://127.0.0.1:{port}"
        with httpx.Client(timeout=3.0) as client:
            root = client.get(f"{base_url}/")
            assert root.status_code == 200
            assert root.json().get("message") == "DataEngineX API"

            health = client.get(f"{base_url}/health")
            assert health.status_code == 200
            assert health.json() == {"status": "alive"}

            ready = client.get(f"{base_url}/ready")
            assert ready.status_code in {200, 503}
            assert "status" in ready.json()
    finally:
        _stop_server(server)
