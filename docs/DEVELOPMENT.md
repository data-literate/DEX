# Development Setup Guide

**Version**: v0.3.5 | **Updated**: Feb 21, 2026

## Prerequisites

- Python 3.11+
- Git
- uv (package manager)
- Cloud credentials only if testing optional cloud adapters (staging/prod)
- Docker (optional)

## Quick Start

```bash
# 1. Clone repo and create feature branch
git clone https://github.com/TheDataEngineX/DEX.git
cd DEX
git checkout -b feat/issue-XXX-description dev

# 2. Install & setup
uv sync
pre-commit install

# 3. Verify setup
uv run poe check-all
```

All tests and linting should pass. You're ready to develop!

## Project Structure

```
DEX/
├── packages/dataenginex/src/dataenginex/  # Main framework package
├── src/careerdex/          # CareerDEX project
├── src/weatherdex/         # Weather reference implementation
├── tests/                  # Test suite
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD pipelines
├── infra/                 # Infrastructure as Code
├── pyproject.toml         # Project config
└── poe_tasks.toml        # Task definitions
```

## Development Workflow

### Branch & Commit

```bash
# 1. Create feature branch from dev
git checkout -b feat/issue-XXX-description dev

# 2. Make changes to src/
# Add tests in tests/

# 3. Format & validate
uv run poe lint
uv run poe typecheck
uv run poe test

# 4. Commit (pre-commit hooks run automatically)
git commit -m "feat(#XXX): description"

# 5. Push & create PR
git push origin feat/issue-XXX-description
```

**PR Requirements:**
- Link to issue: `Closes #XXX`
- All checks pass (CI/CD ~3-5 min)
- 1 approval required
- Merge to `dev` when ready

### Version Management

```bash
# Update version in pyproject.toml (Major.Minor.Patch)
# Push to main to trigger release workflow
git checkout main
git merge --no-ff dev
git push origin main
# Workflow automatically creates tag, release, and Slack notification
```

## Local Data Setup

### Path-Based (Local Dev)
```bash
mkdir -p ~/data/careerdex/{bronze,silver,gold}
mkdir -p ~/data/weather/{bronze,silver,gold}
```

### Optional Cloud Warehouse Adapter (Example: BigQuery)

Use this only when validating the cloud warehouse path; local development can run entirely on path-based storage.

```bash
export GCP_PROJECT=your-dex-project
bq mk --dataset careerdex_bronze
bq mk --dataset careerdex_silver
bq mk --dataset careerdex_gold
```

## Running Pipelines & Tests

### Airflow DAGs
```bash
# Initialize database
airflow db init

# Start webserver (http://localhost:8080)
airflow webserver --port 8080

# In another terminal, start scheduler
airflow scheduler

# Trigger DAG
airflow dags trigger careerdex_job_ingestion

# View logs
airflow tasks logs careerdex_job_ingestion fetch_linkedin 2024-01-01
```

### Testing
```bash
# Run all tests with coverage
uv run poe test-cov

# Run unit tests only
uv run poe test-unit

# Check code quality
uv run poe check-all
```

### Monitoring & Debugging
```bash
# View application logs
tail -f logs/app.log

# Enable debug logging
export LOG_LEVEL=DEBUG
uv run poe dev

# Use Python debugger
python -m pdb src/careerdex/api/main.py

# Prometheus metrics (if running)
open http://localhost:9090
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pre-commit hooks fail | `uv run poe lint-fix` then retry |
| Tests fail locally but pass in CI | Check Python version (3.11+), run `uv sync --reinstall` |
| Import errors | Run `uv sync --reinstall` and restart the shell |
| Airflow DAG not found | Check `src/careerdex/dags/` folder, restart scheduler |

## Common Commands

```bash
uv run poe check-all          # Run lint + typecheck + tests in sequence
uv run poe lint               # Ruff lint check
uv run poe lint-fix           # Auto-fix lint + format
uv run poe typecheck          # mypy strict type checking
uv run poe test               # Run all tests
uv run poe test-cov           # Tests with coverage report
uv run poe security           # pip-audit vulnerability scan
uv run poe pre-commit         # Run all pre-commit hooks
uv run poe dev                # Run dev server (localhost:8000)
uv run poe clean              # Remove caches and build artifacts
```

## Resources & Support

- **Code Style**: See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **ADRs**: See [adr/](./adr/) for architectural decisions
- **Deployment**: See [DEPLOY_RUNBOOK.md](./DEPLOY_RUNBOOK.md)
- **Issues**: [GitHub Issues](https://github.com/TheDataEngineX/DEX/issues)
- **Chat**: #dex-dev Slack channel
