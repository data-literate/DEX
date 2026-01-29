# SDLC Overview

This document defines the software development lifecycle (SDLC) for DEX, including the required stages, artifacts, and quality gates.

## Goals

- Ship deterministic builds with a single immutable image tag per change.
- Enforce quality gates (lint, test, type checks, security scan) on every PR.
- Maintain a complete audit trail for promotion across environments.

## Lifecycle Stages

### 1) Plan

**Entry**: Feature request, bug report, or operational task.

**Activities**:
- Define scope and acceptance criteria.
- Identify impacted services, APIs, or pipelines.
- Track work in GitHub Issues and GitHub Projects (milestones, priorities, owners).

**Exit**: Clear acceptance criteria and implementation plan.

**Artifacts**: GitHub Issue, Project card, checklist of deliverables.

---

### 2) Design

**Entry**: Approved plan.

**Activities**:
- Define interfaces, data contracts, and configuration changes.
- Update architecture or runbook docs if required.

**Exit**: Design reviewed and aligned.

**Artifacts**: Updated documentation, diagrams if applicable.

---

### 3) Implement

**Entry**: Approved design.

**Activities**:
- Develop in a short-lived feature branch.
- Add or update tests.
- Update docs if behavior or interfaces change.

**Exit**: Code complete and locally validated.

**Artifacts**: Code changes, tests, documentation updates.

---

### 4) Verify (CI)

**Entry**: Pull request opened against `dev` (integration) or `main` (release).

**Required Checks**:
- Lint: `ruff check .`
- Formatting: `black --check .`
- Types: `mypy src/`
- Tests: `pytest -v`
- Security: CodeQL and Trivy scans

**Exit**: All checks pass and at least one reviewer approves.

**Artifacts**: CI logs, security scan reports, test results.

---

### 5) Release (CD)

**Entry**:
- Dev deployment: PR merged to `dev`.
- Stage/Prod deployment: PR merged to `main`.

**Actions**:
- Build container image once and tag with commit SHA.
- Push image to registry.
- Update environment manifests via GitOps.

**Exit**: New image tag recorded in git and ArgoCD sync completes.

**Artifacts**: Image tag, git commit updating kustomization, ArgoCD sync history.

---

### 6) Operate

**Entry**: Deployment complete.

**Activities**:
- Monitor application health and logs.
- Respond to alerts and incidents.
- Apply rollback if required.

**Exit**: Service stable and verified.

**Artifacts**: Alerts, logs, incident notes, rollback commits (if any).

## Development Workflow (Summary)

1. Create or update a GitHub Issue and add it to the GitHub Project board.
2. Create a feature branch: `git switch -c feat/short-description`.
3. Implement changes and add tests.
4. Run local checks: `pytest`, `ruff`, `black --check`, `mypy`.
5. Open a PR to `dev` and request review.
6. After validation in dev, open a release PR from `dev` → `main`.
7. Merge after all required checks pass.

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming and PR conventions.
