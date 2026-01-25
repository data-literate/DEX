SDLC Overview

Short lifecycle overview for DEX

1. Plan: issues and design on feature branch
2. Develop: short-lived feature branches, unit tests and linting
3. CI: run lint, tests, type checks on PRs
4. Merge: PRs merged to `main` when CI passes and reviewers approve
5. CD: artifact built once and promoted to dev → staging → prod
6. Monitor: health checks, alerts, and runbooks

Use the `CONTRIBUTING.md` for branch names and PR conventions.
