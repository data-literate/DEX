# Development Setup Guide

**Version**: v0.3.0 | **Updated**: Feb 15, 2026

## Prerequisites

- Python 3.11+
- Git
- uv (package manager)
- GCP credentials (staging/prod only)
- Docker (optional)

## Quick Start

```bash
# 1. Clone repo and create feature branch
git clone https://github.com/data-literate/DEX.git
cd DEX
git checkout -b feat/v0.2.0-your-feature dev

# 2. Install & setup
uv sync
pre-commit install

# 3. Verify setup
poe check-all
```

All tests and linting should pass. You're ready to develop!

## Project Structure

```
DEX/
├── src/dataenginex/        # Main framework
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
poe lint
poe typecheck
poe test

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

### BigQuery (GCP)
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
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_pipelines_careerdex.py -v

# Check code quality
poe check-all
```

### Monitoring & Debugging
```bash
# View application logs
tail -f logs/app.log

# Enable debug logging
export LOG_LEVEL=DEBUG
python -m src.dataenginex.main

# Use Python debugger
python -m pdb src/dataenginex/main.py

# Prometheus metrics (if running)
open http://localhost:9090
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pre-commit hooks fail | `poe format` then retry |
| Tests fail locally but pass in CI | Check Python version (3.11+), run `uv sync --reinstall` |
| Import errors | Run `uv sync` and set `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"` |
| Airflow DAG not found | Check `src/careerdex/dags/` folder, restart scheduler |

## Common Commands

```bash
poe check-all          # Run lint + typecheck + tests in sequence
poe lint               # Ruff lint check
poe lint-fix           # Auto-fix lint + format
poe typecheck          # mypy strict type checking
poe test               # Run all tests
poe test-cov           # Tests with coverage report
poe security           # pip-audit vulnerability scan
poe pre-commit         # Run all pre-commit hooks
poe dev                # Run dev server (localhost:8000)
poe clean              # Remove caches and build artifacts
```

## Resources & Support

- **Code Style**: See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Architecture**: See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **ADRs**: See [docs/adr/](./docs/adr/) for architectural decisions
- **Deployment**: See [docs/DEPLOY_RUNBOOK.md](./docs/DEPLOY_RUNBOOK.md)
- **Issues**: [GitHub Issues](https://github.com/data-literate/DEX/issues)
- **Chat**: #dex-dev Slack channel
