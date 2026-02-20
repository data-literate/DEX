---
applyTo: "tests/**/*.py"
---

# Testing — Project Specifics

## Commands
- `poe test` | `poe test-unit` | `poe test-integration` | `poe test-cov`
- `asyncio_mode = "auto"` — no need for `@pytest.mark.asyncio`
- Warnings treated as errors (except uvicorn/websockets deprecations)

## Organization
- `tests/unit/` — isolated (mock externals) | `tests/integration/` — live uvicorn server
- `conftest.py` has minimal shared fixtures — tests create local fixtures and `TestClient` instances

## Naming
- File: `test_<module>.py` | Class: `Test<Component>` | Function: `test_<what_it_tests>`

## Test Clients
- **Sync**: `TestClient` from Starlette (most unit tests)
- **Async**: `httpx.AsyncClient` with `ASGITransport` (async endpoint tests)
- **Integration**: `_run_server()` spawns real uvicorn on random port in daemon thread

## Patterns
- `@pytest.mark.parametrize` for input variations | `tmp_path` for temp files
- Group related tests in `Test<Component>` classes (see `test_ml.py`, `test_health.py`)
- Scope fixtures appropriately (function, module, session)
