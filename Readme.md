# DEX  DataEngineX

This repository contains **DEX (DataEngineX)**, a Python-based data engineering and ML platform with **production-ready CI/CD and GitOps automation**.

## Quick Links
- **Local Development**: See [Quick Start](#quick-start-local) below
- **Infrastructure & Kubernetes**: See [infra/README.md](infra/README.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Project Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Package Manager | Poetry |
| Web API | FastAPI with Uvicorn |
| Code Quality | Ruff, Black, MyPy |
| Testing | Pytest |
| **Container** | **Docker, ghcr.io registry** |
| **Kubernetes** | **ArgoCD, Kustomize, Multi-environment** |
| **CI/CD** | **GitHub Actions (fully automated)** |

## Repository Structure

```
DEX/
 src/dataenginex/          # Main application package
 tests/                    # Unit and integration tests
 pipelines/weather/        # Example data pipelines
 learning/                 # Python concept modules
 infra/argocd/             # Kubernetes manifests (GitOps)
 docs/                     # Runbooks and guides
 .github/workflows/        # CI/CD automation
 pyproject.toml            # Poetry configuration
 Dockerfile                # Container image build
```

## Quick Start (Local)

### Prerequisites
- Git, Python 3.11+, Poetry
- (Optional) Docker for running containerized app

### 1. Clone & Install

```bash
git clone https://github.com/data-literate/DEX
cd DEX
poetry install
```

### 2. Run the API

```bash
poetry run uvicorn dataenginex.main:app --reload
```

Visit **http://127.0.0.1:8000** to verify the health endpoint.

### 3. Run Tests

```bash
poetry run pytest -v
```

### 4. Run Code Quality Checks

```bash
poetry run ruff check .
poetry run black --check .
poetry run mypy src/
```

## CI/CD Pipeline Overview

Every commit to `main` triggers an automated pipeline:

### 1. **CI Workflow** (Continuous Integration)
- **Lint** (ruff, black, mypy) → catch code quality issues
- **Test** (pytest) → run unit and integration tests
- **Build** Docker image with commit SHA tag (`sha-{commit}`)
- **Push** to `ghcr.io/data-literate/dex`

### 2. **CD Workflow** (Continuous Deployment)
- **Update** dev environment manifest with new image tag
- **Commit** changes back to repository automatically
- **Security Scan** (Trivy, CodeQL) for vulnerabilities

### 3. **ArgoCD Auto-Sync**
- **Detects** git changes to manifests
- **Syncs** to Kubernetes (dev → stage → prod)
- **Validates** deployment health

See [infra/README.md](infra/README.md) for detailed architecture.

## Multi-Environment Deployment

All three environments deploy automatically via ArgoCD:

| Environment | Replicas | Namespace | Status |
|---|---|---|---|
| **dev** | 2 | `dex-dev` | Synced & Healthy  |
| **stage** | 2 | `dex-stage` | Synced & Healthy  |
| **prod** | 3 | `dex-prod` | Synced & Healthy  |

**Branch Protection on `main`:**
- Pull request review required
- Status checks pass (CI, Security Scan)
- Branches up to date before merge
- No force pushes or deletions

## Local Kubernetes Testing

To test ArgoCD deployments locally:

```bash
# Start ArgoCD
kubectl apply -f infra/argocd/application.yaml

# Check application status
kubectl get application -n argocd

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Visit https://localhost:8080
```

See [docs/LOCAL_K8S_SETUP.md](docs/LOCAL_K8S_SETUP.md) for detailed setup instructions.

## Documentation

**Core Documentation:**
- **[docs/README.md](docs/README.md)**  Start here: repository tour, workflows, and key references
- **[infra/README.md](infra/README.md)**  Kubernetes architecture, kustomize overlays, ArgoCD workflows
- **[CONTRIBUTING.md](CONTRIBUTING.md)**  Development workflow and PR process
- **[docs/SDLC.md](docs/SDLC.md)**  Software development lifecycle and branching strategy
- **[docs/DEPLOY_RUNBOOK.md](docs/DEPLOY_RUNBOOK.md)**  Release and rollback runbook
- **[docs/monitoring.md](docs/monitoring.md)**  Monitoring and alerting setup

## Development Workflow

This repository follows a gated workflow: local checks → PR review → automated CI/CD. Work is tracked using GitHub Issues and GitHub Projects. For full lifecycle details, see [docs/SDLC.md](docs/SDLC.md).

### Day-to-Day Steps

1. Create or update a GitHub Issue and add it to the GitHub Project board
2. Create a feature branch: `git switch -c feat/short-description`
3. Implement changes and add/update tests
4. Run local checks:
	- `poetry run pytest -v`
	- `poetry run ruff check .`
	- `poetry run black --check .`
	- `poetry run mypy src/`
5. Open a PR to `dev` and request review (deploys to dev environment)
6. After validation in dev, open a release PR from `dev` → `main`
7. Merge after required checks pass (deploys to stage/prod)

### Required Gates

- CI checks must pass (lint, formatting, type check, tests, security scan)
- At least one reviewer approval
- Branch must be up to date with the target branch (`dev` or `main`)

## Useful Commands

```bash
# Install dependencies
poetry install

# Run app locally
poetry run uvicorn dataenginex.main:app --reload

# Run tests
poetry run pytest -v

# Run all quality checks
poetry run ruff check .
poetry run black --check .
poetry run mypy src/

# Auto-format code
poetry run black .

# Build Docker image locally
docker build -t dex:latest .

# Run Docker image
docker run -p 8000:8000 dex:latest
```

## Next Steps

1. **For local development**: Follow the Quick Start above
2. **For Kubernetes/ArgoCD testing**: See [docs/LOCAL_K8S_SETUP.md](docs/LOCAL_K8S_SETUP.md)
3. **For infrastructure details**: See [infra/README.md](infra/README.md)
4. **For contributing code**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Status**: Production-ready CI/CD pipeline  | All environments synced & healthy  | Ready for development 

