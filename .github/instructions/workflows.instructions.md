---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
---

# GitHub Actions — Project Specifics

## Workflows
- `ci.yml` — ruff + mypy + pytest on push/PR to main/dev
- `cd.yml` — Docker build + push to ghcr.io (after CI success)
- `release-dataenginex.yml` — DataEngineX package release (tag + GitHub release)
- `release-careerdex.yml` — CareerDEX app release (tag + GitHub release)
- `pypi-publish.yml` — DataEngineX PyPI publishing (triggered by DataEngineX release)
- `package-validation.yml` — Validate DataEngineX wheel build + twine
- `security.yml` — Semgrep + CodeQL on push/PR to main/dev

## Naming
- Files: lowercase `.yml` | Workflows: title case | Jobs: kebab-case | Steps: sentence case

## Patterns
- `actions/checkout@v6` | `actions/github-script@v7` for Slack via `SLACK_WEBHOOK`
- `uv` for deps (not pip) | Python 3.11 | `ubuntu-latest`
- Declare `permissions:` per workflow — pin action versions to tags
- CD triggers on `workflow_run` after CI success
- Matrix releases: separate workflows for independent package versioning

