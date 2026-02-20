---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
---

# GitHub Actions — Project Specifics

## Workflows
- `ci.yml` — ruff + mypy + pytest on push/PR to main/dev
- `cd.yml` — Docker build + push to ghcr.io (after CI success)
- `release.yml` — git tag + GitHub release on pyproject.toml change
- `security.yml` — Semgrep + CodeQL on push/PR to main/dev

## Naming
- Files: lowercase `.yml` | Workflows: title case | Jobs: kebab-case | Steps: sentence case

## Patterns
- `actions/checkout@v6` | `actions/github-script@v7` for Slack via `SLACK_WEBHOOK`
- `uv` for deps (not pip) | Python 3.11 | `ubuntu-latest`
- Declare `permissions:` per workflow — pin action versions to tags
- CD triggers on `workflow_run` after CI success
