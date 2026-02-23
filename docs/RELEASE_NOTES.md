# Release Notes — 2026-02-11

## Highlights
- **SLO-aware monitoring**: Alerting rules now track latency, error rates, and saturation per environment, routed through Alertmanager runsbooks aligned with the SLO definitions documented in `infra/prometheus/alerts/dataenginex-alerts.yml` and `infra/alertmanager`.
- **Environment-labeled metrics**: The Prometheus client now exports all HTTP counters, histograms, and gauges with an `environment` label so dashboards & alerts can differentiate `dev`/`stage`/`prod` workloads without duplicating services.
- **Pyconcepts-facing API**: Added `/api/external-data` (wraps `pyconcepts.external_data.fetch_external_data`) and `/api/insights` (text/event-stream) so downstream runners can consume the helper data + streaming insights from `pyconcepts`.
- **Docs/tests**: `tests/test_main.py` and `tests/test_metrics.py` cover the new endpoints and metrics labels, and the documentation now explains how to validate the new alerts and APIs.

## Verification checklist
1. `uv run poe lint` – fast pass of Ruff/mypy checks (already green).
2. `./.venv/bin/pytest -v` – 31 tests including the new endpoints now pass.
3. `docker compose build` – confirms the multi-stage Dockerfile still builds the image after these changes.

Bring this note into the release PR so QA sees what changed in v1.0.0.