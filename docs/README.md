# DEX — Single Documentation

This single documentation file consolidates project guidance, quick-run instructions, conceptual notes, and the folder structure. Use this as the canonical developer guide while you explore and extend DEX.

---

## Project Overview

DEX (DataEngineX) is a Python-based Data & AI Engine demonstrating end-to-end workflows in data engineering, analysis, ML, generative AI, MLOps, and DevOps. The repository contains small, focused concept modules under `src/pyconcepts/` designed for learning and integration into runnable examples.

## Quick Start — How to Run Locally

Prerequisites
- Python 3.10+ (3.12 used in this workspace)
- Virtual environment tool (venv, poetry, or pipenv)

Install dependencies (using pip):

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the FastAPI application (development):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Run tests:

```bash
pytest -q
```

Notes
- If you use Poetry, run `poetry install` and `poetry run uvicorn app.main:app --reload`.
- Ensure environment variables (API keys, DB URLs) are set via a `.env` file when needed.

---

## `src/pyconcepts` — Modules, Goals and Exercises

This section documents each small concept module and suggests concrete exercises to integrate them end-to-end into DEX.

- `async_http_client.py`
	- Goal: implement a robust async HTTP client with retries, timeouts, and simple in-memory caching.
	- Exercise: fetch live data from a public API (OpenWeatherMap, Coindesk, etc.), cache results for 60 seconds, expose via an endpoint `/api/external-data`.

- `async_dependency_injection.py`
	- Goal: show how to wire services (HTTP client, DB connection, config) into FastAPI using dependency injection.
	- Exercise: create factory functions that return DB or client instances; add tests that replace dependencies with mocks to verify behavior.

- `context_managers.py`
	- Goal: implement sync/async context managers for resource management (DB connections, temporary files, timers).
	- Exercise: add a DB connection context manager for SQLite that opens/closes connections and times queries.

- `strict_decorators.py`
	- Goal: provide decorators for input validation, retry/backoff, and simple rate limiting.
	- Exercise: add a `@retry` decorator used by the HTTP client; add a `@validate_types` decorator with runtime checks used in a utility function.

- `var_len_args.py`
	- Goal: demonstrate flexible function signatures and safe argument handling.
	- Exercise: implement a small ETL helper that accepts variable transform functions and applies them to a DataFrame.

- `yield_keyword.py`
	- Goal: explain and demonstrate generator patterns and streaming results.
	- Exercise: implement a streaming CSV reader that yields rows to an async endpoint using `StreamingResponse` from FastAPI.

### Integrations (end-to-end ideas)

- Build a small ETL endpoint `/api/insights`:
	1. Use the async HTTP client to fetch raw data.
	2. Use `var_len_args` transforms to clean/aggregate data.
	3. Store results in SQLite via `context_managers` DB context.
	4. Expose aggregated results and stream raw rows with `yield_keyword` utilities.

### Testing ideas

- Create unit tests for the DI layer by injecting mock HTTP clients.
- Test retry behavior by simulating failing endpoints.

---

## Folder Structure

Current (trimmed):

```
/ (project root)
├─ app/
│  └─ main.py
├─ src/pyconcepts/
│  ├─ async_dependency_injection.py
│  ├─ async_http_client.py
│  ├─ context_managers.py
│  ├─ strict_decorators.py
│  ├─ var_len_args.py
│  └─ yield_keyword.py
├─ tests/
├─ requirements.txt
└─ Readme.md
```

Proposed additions (recommended):

```
docs/                 # consolidated project documentation (this file)
examples/             # small runnable examples (weather, ETL)
notebooks/            # Jupyter notebooks for EDA and experiments
infra/                # Docker, GitHub Actions, Terraform
pipelines/            # Prefect/Airflow pipeline definitions
```

Guidance
- Keep `docs/` targeted and small while you iterate.
- Add runnable examples next to lessons (e.g., `examples/weather/`).

---

## Quick Win Example Suggestion

Create a **Weather Data API**:
- Fetch weather from OpenWeatherMap API (free tier)
- Cache in SQLite
- Serve via FastAPI endpoints
- Add tests and structured logging
- Use the concept modules (`async_http_client`, DI, context managers, streaming) to demonstrate E2E flow

---

If you want, I can now:
- update the root `Readme.md` to link to this file, and
- add a small runnable example under `examples/weather/` with code, tests, and a short README.
