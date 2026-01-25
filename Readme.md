# DEX — DataEngineX

This repository contains DEX (DataEngineX), a Python-based data engineering and ML example platform.
**This README** summarizes how to set up, develop, test, and deploy the project, and describes the project's CI/CD and SDLC practices.

**Contents**
- Project overview
- Quick start
- Development workflow
- Tests & linters
- CI/CD and SDLC
- Collaboration & contributing
**Project overview**

- Language: Python (>=3.11)
- Packaging: Poetry
- Web API: FastAPI
- Runners: Uvicorn
- Linting / formatting: Ruff, Black
- Type checking: MyPy
- Tests: Pytest

Repository layout (high-level)
- `src/` — application package `dataenginex`
- `app/` — legacy app entrypoints (migrated)
- `pipelines/` — example data pipelines
- `tests/` — unit tests
- `infra/` — infrastructure/IaC skeleton
- `docs/` — documentation and runbooks
Quick start (local)

Prerequisites: Git, Python 3.11+, Poetry, pipx (optional)
1. Clone the repository

```bash
git clone <repo-url>
cd DEX
```
2. Install dependencies (development environment)

```bash
poetry install
```
3. Run the API locally

```bash
poetry run uvicorn dataenginex.main:app --reload
```
Visit http://127.0.0.1:8000/ to see the health endpoint.

---
Development workflow

- Create a short-lived feature branch from `main`: `git switch -c feat/JIRA-123-description`.
- Work locally and run linters/tests frequently.
- Open a pull request (PR) against `main` when ready. PRs should have at least one reviewer and pass CI.
- Use semantic version tags for releases (e.g. `v1.2.0`).

Branching rules (recommended)
- `main` — protected; only mergeable when CI passes and approvals are in place.
- `feature/*`, `fix/*` — short-lived branches for changes.
- Releases: create annotated tags and optionally `release/*` branches if needed.
---

Tests & linters

- Run linters and type checks locally:
```bash
poetry run ruff .
poetry run black --check .
poetry run mypy . --ignore-missing-imports
```

- Apply automatic formatting:
```bash
poetry run black .
```
- Run tests:

```bash
poetry run pytest -q
```
There is a `poe lint` task (Poethepoet) that runs the standard linting sequence:

```bash
poe lint
```
---

CI/CD and SDLC (summary)

- CI runs on PRs and pushes: installs dependencies, runs linters, type checks, unit tests, and builds artifacts.
- Artifacts (wheel or Docker image) are built once and promoted across environments.
- Environments: `dev` (auto-deploy), `staging` (post-merge), `prod` (manual approval required).
- Security: dependency scanning (Dependabot/renovate, Snyk), SAST (semgrep/bandit), and secret scanning should be enabled in CI.
- IaC and manifests live under `infra/` and `deploy/` (skeletons available).

Example GitHub Actions files are available in `.github/workflows/` to run CI and deployments; adjust registry and secrets for your provider.
---

Collaboration & contributing

- Please follow the `CONTRIBUTING.md` guidelines for commit messages, PR size, and testing requirements.
- Use the PR template to describe the change, testing performed, and any manual steps.
- `CODEOWNERS` enforces code review by owners for critical directories.

Recommended PR checklist:
- [ ] Tests added or updated
- [ ] Linting and formatting passed
- [ ] Type checks passing
- [ ] Documentation updated (if applicable)

---

Useful commands

- Install deps: `poetry install`
- Run app: `poetry run uvicorn dataenginex.main:app --reload`
- Run tests: `poetry run pytest -q`
- Run linters: `poetry run ruff . && poetry run black --check . && poetry run mypy . --ignore-missing-imports`
- Format code: `poetry run black .`

---

Where to go next

- To enable CI: add repository secrets (DOCKER_REGISTRY, CLOUD_CREDENTIALS) and review `.github/workflows/ci.yml`.
- To deploy: configure the CD workflow with your cloud provider credentials and target cluster.
- To contribute: read `CONTRIBUTING.md` and open a small PR following the template.

If you want, I can scaffold the suggested CI and CD workflows, PR templates, and `CONTRIBUTING.md` next.
# DEX — DataEngineX

**DEX (DataEngineX)** is a comprehensive, **Python-based Data & AI Engine** designed to demonstrate end-to-end workflows in **data engineering, data analysis, machine learning, deep learning, generative AI, MLOps, and DevOps**.  

This project is built to serve as a **portfolio-ready, open-source platform**, showcasing modern Python data workflows, production-style pipelines, automated ML operations, and scalable deployment practices.

---

## 🚀 Project Overview

DEX aims to demonstrate the **full lifecycle of Python-based data projects**:

1. **Data Collection & Engineering** – Acquire, clean, transform, and store data.  
2. **Exploratory Data Analysis (EDA) & Visualization** – Analyze datasets and extract insights.  
3. **Machine Learning & Deep Learning** – Build classical ML models, neural networks, and LLM pipelines.  
4. **Pipelines & Workflow Automation** – Python-based ETL, ML, and AI workflows.  
5. **MLOps** – Experiment tracking, model versioning, CI/CD, and automated retraining.  
6. **DevOps & Deployment** – Containerized APIs, cloud-ready services, monitoring, and logging.  
7. **Experimentation & Documentation** – Reproducible notebooks, reports, and dashboards for all phases.

DEX is **extensible**, allowing integration of new datasets, models, and AI technologies as learning progresses.

---


## 💡 Key Features

### **Data Engineering & Analysis**
- Python-based ETL pipelines for ingestion and transformation on **Databricks**  
- Databricks notebooks for collaborative data engineering and analysis  
- Feature engineering and preprocessing  
- Exploratory Data Analysis (EDA) with **Matplotlib, Seaborn, Plotly**  
- Dataset versioning and management

### **Machine Learning & Deep Learning**
- Classical ML models: **scikit-learn, XGBoost, LightGBM**  
- Deep Learning models: **TensorFlow, PyTorch**  
- Generative AI / LLMs: **HuggingFace Transformers, LangChain, OpenAI API**  
- Hyperparameter tuning and evaluation

### **Pipelines & Automation**
- Python scripts for end-to-end workflows  
- Orchestration using **Prefect or Airflow**  
- Modular pipelines for reproducibility

### **MLOps**
- Experiment tracking: **MLflow, Weights & Biases**  
- Model versioning, retraining, and deployment triggers  
- Metrics dashboards for model performance monitoring  
- Reproducibility and logging best practices

### **DevOps & Deployment**
- Containerized services using **Docker**  
- REST APIs using **FastAPI or Flask**  
- Cloud-ready deployment on **AWS / GCP / Azure**  
- Automated CI/CD pipelines using **GitHub Actions**  
- Logging and monitoring dashboards

### **Portfolio & Documentation**
- Organized notebooks and scripts for each phase  
- Experiment tracking and reporting  
- Interactive dashboards for insights and metrics

---

## 🧰 Python Tech Stack & Open-Source Tools

| Area                        | Tools / Technologies                           |
|-------------------------------|-----------------------------------------------|
| Data Processing               | Python, Apache PySpark, Pandas, NumPy, Databricks         |
| ETL / Pipelines               | Python scripts, Airflow, Prefect, Databricks Workflows             |
| Storage                       | SQLite, PostgreSQL, Parquet, Databricks Delta Lake                  |
| Machine Learning              | scikit-learn, XGBoost, LightGBM             |
| Deep Learning / AI            | PyTorch, TensorFlow, HuggingFace, LangChain |
| Visualization                 | Matplotlib, Seaborn, Plotly                  |
| MLOps / Experiment Tracking   | MLflow, Weights & Biases, DVC               |
| Deployment & APIs             | FastAPI, Flask, Docker                        |
| CI/CD / DevOps                | GitHub Actions, Docker, Terraform (optional) |
| Monitoring / Logging          | MLflow dashboards, Prometheus/Grafana, Python logging |

---

## 📌 How to Get Started

1. **Clone the repository**

```bash
git clone https://github.com/data-literate/DEX.git
cd DEX
python3 -m pip install pipx
python3 -m pipx ensurepath
pipx install uv poethepoet poetry

poetry lock
poetry install
poetry env list

poetry run uvicorn dataenginex.main:app --host 127.0.0.1 --port 8000 --reload