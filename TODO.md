# TODO

## Priorities (proposed owners / target windows)
- Week 1-2 — Platform: CI pipeline (lint/type/test/build/push), Docker image build and push, SonarQube/SonarCloud wiring, Docker Desktop K8s setup.
- Week 2-3 — Platform/DevOps: Local ArgoCD setup, git repo + manifests, kustomize overlays, image updater testing, local workflow documentation.
- Week 2-3 — Architecture: Define module boundaries, implement separation of concerns, module interfaces, shared data layer strategy.
- Week 1-2 — Backend: Health/readiness probes, graceful shutdown, structured logging with request IDs, basic metrics/tracing.
- Week 2-3 — Backend: E2E API test via uvicorn, unit tests for FastAPI and `src/pyconcepts` modules.
- Week 2-4 — Backend: Implement `pyconcepts` exercises and expose `/api/external-data` and `/api/insights` endpoints.
- Week 2-3 — Platform/DevOps (continued): ArgoCD cluster setup (staging/prod), ApplicationSet, image updater automation, notifications, RBAC.
- Week 3-4 — Architecture: Dependency mapping, service extraction criteria, identify first extraction candidate, document strategy.
- Week 3-4 — Data/ML: Experiment tracking + model registry (MLflow/W&B), model serving/monitoring plan, retraining job spec.
- Week 3-4 — DataOps: Data quality framework, orchestration (Airflow/Prefect), pipeline observability and testing.
- Week 3-4 — Data Engineering: Incremental processing, partitioning, transformation testing, feature engineering library.
- Week 3-4 — MLOps: ML CI/CD pipeline, model versioning/monitoring/serving, automated retraining triggers.
- Week 3-5 — Data Science: Experiment tracking workspace, feature selection, model comparison, cross-validation.
- Week 3-5 — Platform/SRE: Caching layer (Redis/memory) and rate limiting; alerting and dashboards tied to SLOs.
- Week 4-6 — Data Analysis: BI tool integration (Metabase/Superset), semantic layer, automated reporting, visualization.
- Week 4-6 — Security: AuthN/AuthZ (OIDC/JWT), dependency/container scanning, secret management/rotation, harden headers.
- Week 5+  — Architecture: Messaging/queueing plan, DR (RTO/RPO, backups), SLO/SLI/SLA definitions, load-balancing strategy.
- Week 5+  — Research: Microservices architecture, service mesh, distributed patterns, serverless ML, cost optimization.

## Immediate: CI/CD and Quality
- [ ] Add GitHub Actions CI to run lint, type-check, and tests; build and push a Docker image tagged with the commit SHA (plus `latest` on `main`). [P1 W1-2]
- [ ] Set up ArgoCD cluster and repository structure for GitOps-driven deployments. [P1 W2-3]
- [ ] Replace manual Helm deployment with ArgoCD ApplicationSet for multi-env promotion (dev → staging → prod). [P1 W2-3]
- [ ] Add git-based configuration repo (separate from source) with kustomize overlays per environment. [P1 W2-3]
- [ ] Stand up SonarQube (AWS or SonarCloud), run scans in CI, and hook results to GitHub PRs. [P1 W1-2]

## Testing
- [ ] Expand unit tests for FastAPI entrypoints and `src/pyconcepts` modules; target measurable coverage. [P1 W2-3]
- [ ] Add an integration test that exercises the API end-to-end (startup via uvicorn) with a sample request payload. [P1 W2-3]

## Local Development & Testing (Docker Desktop + ArgoCD)
- [ ] Set up Docker Desktop with Kubernetes enabled; verify cluster connectivity via kubectl. [P1 W1-2]
- [ ] Install ArgoCD in local K8s cluster; port-forward UI and verify Web access. [P1 W2-3]
- [ ] Create local git repository (or GitHub fork) with Helm/kustomize manifests for DEX service. [P1 W2-3]
- [ ] Build and push Docker image to local registry (Docker Desktop) with SHA tag. [P1 W2-3]
- [ ] Define ArgoCD Application manifest pointing to local git repo; verify auto-sync to cluster. [P1 W2-3]
- [ ] Create kustomize base + dev/staging overlays for local testing (different replicas, resource limits). [P1 W2-3]
- [ ] Test ApplicationSet with parameter substitution across dev/staging environments locally. [P2 W2-4]
- [ ] Set up ArgoCD Image Updater to detect new image tags and auto-update local manifests. [P2 W2-4]
- [ ] Configure local webhook for deployment notifications (mock Slack via RequestBin or similar). [P2 W3-4]
- [ ] Test rollback workflow: revert commit in git → ArgoCD syncs to previous version. [P2 W3-4]
- [ ] Test manual vs. automated sync policies; verify health checks and resource status. [P2 W3-4]
- [ ] Document local GitOps workflow: setup guide, common commands (argocd app sync/rollback), troubleshooting. [P1 W2-3]
- [ ] Create Docker Compose override for local dev (alternative to local K8s for fast iteration). [P2 W3-5]

## Application and Examples
- [ ] Implement the `pyconcepts` exercises: async HTTP client with retries/cache, DI wiring, context managers, decorators, and streaming helpers; expose a sample `/api/external-data` endpoint. [P1 W2-4]
- [ ] Add a streaming ETL endpoint `/api/insights` that uses transform pipelines (`var_len_args`) and streaming responses (`yield_keyword`). [P1 W2-4]
- [ ] Create a runnable `examples/weather/` FastAPI example that surfaces the weather pipeline outputs. [P1 W2-4]

## Documentation
- [ ] Reconcile the root Readme with `docs/README.md`; link the single-doc guide and remove duplicated sections. [P1 W1-2]
- [ ] Add a short "how to run" snippet for the weather pipeline and reference the execution checklist. [P1 W1-2]

## Architecture and System Design
- [ ] Define system context and deployment topology (API service + data pipelines + model serving) with diagrams. [P3 W5+]
- [ ] Document service boundaries and contracts for REST/GraphQL/gRPC; pick the default external surface. [P3 W5+]
- [ ] Specify persistence choices (OLTP DB, object storage, cache) and retention policies. [P3 W5+]
- [ ] Add messaging/queueing plan (Kafka/RabbitMQ/SQS) for async workloads and retries. [P3 W5+]
- [ ] Design API rate limiting, pagination, idempotency, and versioning strategy. [P2 W3-5]
- [ ] Describe backpressure, timeouts, and circuit breaker policies for upstream calls. [P2 W3-5]
- [ ] Capture scaling plan: vertical vs. horizontal; HPA settings; resource requests/limits; GitOps-driven autoscaling. [P3 W5+]
- [ ] Add disaster recovery/RTO-RPO targets, backup/restore runbook, and DR test cadence (backup git state and ArgoCD state). [P3 W5+]
- [ ] Define SLO/SLI/SLA for latency, availability, and error budget policies. [P2 W3-5]
- [ ] Document GitOps architecture: git source of truth, ArgoCD reconciliation, and promotion pipelines. [P1 W2-3]

## Production Hardening
- [ ] Add centralized config/secrets management (12-factor; .env for dev, cloud secret manager for prod). [P3 W4-6]
- [ ] Add structured logging, request IDs, and correlation IDs; standard log fields. [P1 W1-2]
- [ ] Add metrics (Prometheus/OpenTelemetry) for requests, dependencies, and business events. [P1 W1-2]
- [ ] Add tracing (OpenTelemetry) spans for API, DB, cache, and external calls. [P1 W1-2]
- [ ] Add health/readiness/liveness probes; graceful shutdown hooks. [P1 W1-2]
- [ ] Add caching strategy (per-request cache headers + Redis/memory) with invalidation rules. [P2 W3-5]
- [ ] Add feature flags/toggles for risky changes. [P2 W3-5]
- [ ] Add data validation/quality checks on pipeline inputs and model features. [P2 W3-5]
- [ ] Add blue/green or canary deployment steps in CD. [P2 W3-5]

## Data and ML Platform
- [ ] Add storage layout for raw/bronze/silver/gold layers; schema registry where relevant. [P3 W5+]
- [ ] Add data catalog/lineage tool (e.g., OpenMetadata/Amundsen/Marquez). [P3 W5+]
- [ ] Add experiment tracking and model registry (MLflow/W&B) with promotion workflow. [P1 W3-4]
- [ ] Add model serving plan (batch + real-time) and monitoring for drift/performance. [P1 W3-4]
- [ ] Add scheduled retraining job spec and dependency on fresh features. [P1 W3-4]

## Security and Compliance
- [ ] Add authentication/authorization plan (OIDC/JWT) and roles for API/pipelines. [P3 W4-6]
- [ ] Add secrets rotation policy and least-privilege IAM roles for CI/CD and runtime. [P3 W4-6]
- [ ] Add dependency scanning (Dependabot/Renovate), SAST (semgrep/bandit/ruff rules), and container scan. [P3 W4-6]
- [ ] Add input validation and safe defaults for HTTP headers (CORS, CSP, HSTS if applicable). [P3 W4-6]

## Observability and Ops Tooling
- [ ] Add dashboarding for logs/metrics/traces (Grafana/Loki/Tempo or cloud equivalents). [P2 W3-5]
- [ ] Add alerting rules tied to SLOs (latency, error rate, saturation) and on-call rotation. [P2 W3-5]
- [ ] Add runbook links for common failures (deploy fails, DB unavailable, upstream timeout). [P2 W3-5]

## GitOps & ArgoCD
- [ ] **Create separate git repository (dex-gitops-config) for ArgoCD manifests and kustomize overlays** — DO NOT mix with application source. [P1 W1-2]
- [ ] Stand up ArgoCD cluster in target Kubernetes environment (dev, staging, prod). [P1 W2-3]
- [ ] Create git repository for infrastructure-as-code (separate from application source); initialize with kustomize structure. [P1 W2-3]
- [ ] Define ArgoCD Application manifests for DEX service + dependencies (PostgreSQL, Redis, etc.); use application.yaml as template. [P1 W2-3]
- [ ] Add ApplicationSet for multi-environment promotion with parameter substitution (image tag, replicas, etc.). [P1 W2-3]
- [ ] Implement kustomize base + overlays for dev/staging/prod with environment-specific configs in gitops-config repo. [P1 W2-3]
- [ ] Add image update automation (ArgoCD Image Updater) to deploy new SHA-tagged images. [P2 W2-4]
- [ ] Integrate CI (GitHub Actions) to commit new image tags to config repo on successful builds. [P2 W2-4]
- [ ] Add health checks and sync policies (automated vs. manual) per environment. [P2 W3-4]
- [ ] Configure ArgoCD notifications to Slack/email on deployment success/failure. [P2 W3-4]
- [ ] Add RBAC and secret management in ArgoCD (sealed-secrets or External Secrets Operator). [P2 W3-5]
- [ ] Document GitOps workflow: commit → CI builds → config repo update → ArgoCD syncs. [P1 W2-3]
- [ ] Add ArgoCD UI dashboards for deployment visibility and rollback capabilities. [P2 W3-4]
- [ ] Set up PR preview ApplicationSet with pullRequest generator for ephemeral test environments. [P1 W2-3]
- [ ] Add 'preview' label requirement for PR preview environments to avoid overhead. [P2 W2-3]

## GitOps Promotion Workflow (Gold Standard: Build Once, Promote Same Artifact)
- [ ] **CI builds Docker image tagged with commit SHA** (e.g., `sha-4f2c9a1`) on every push. [P1 W1-2]
- [ ] **CI updates gitops-config repo** dev overlay with new SHA after successful build/test. [P1 W2-3]
- [ ] ArgoCD auto-syncs dev environment with new SHA (test in dev first). [P1 W2-3]
- [ ] Create promotion script/workflow to copy SHA from dev → staging overlay (manual or automated after QA sign-off). [P1 W2-3]
- [ ] ArgoCD auto-syncs staging with promoted SHA (validation in staging). [P1 W2-3]
- [ ] Create production promotion workflow: manual approval + copy SHA from staging → prod overlay. [P1 W2-3]
- [ ] ArgoCD syncs prod with approved SHA (manual sync policy enforced). [P1 W2-3]
- [ ] Add Git audit trail: tag promotion commits with env + approver + timestamp. [P2 W3-4]
- [ ] Document promotion flow: dev (auto) → staging (QA approval) → prod (manual approval). [P1 W2-3]
- [ ] Add rollback procedure: revert overlay commit → ArgoCD syncs previous SHA. [P2 W3-4]
- [ ] Create promotion dashboard/CLI tool to visualize which SHA is in each environment. [P2 W3-5]
- [ ] Add automated smoke tests in dev before allowing promotion to staging. [P2 W3-5]
- [ ] Add staging validation gates (performance, security scans) before prod promotion. [P2 W3-5]

## DataOps (Data Quality & Orchestration)
- [ ] Add data quality framework: schema validation, constraint checks, anomaly detection on ingestion. [P1 W3-4]
- [ ] Add data profiling on raw and processed datasets (statistics, nulls, distributions). [P2 W3-5]
- [ ] Add data lineage tracking (source → transform → destination) across pipelines. [P2 W3-5]
- [ ] Add orchestration (Airflow/Prefect/Dagster) with DAG definitions for weather and future pipelines. [P1 W3-4]
- [ ] Add data versioning strategy (DVC/lakeFS) for reproducibility and rollback. [P2 W4-6]
- [ ] Add automated data reconciliation checks (source vs. target counts, checksums). [P2 W4-6]
- [ ] Add data freshness monitoring and SLAs (data arrival time, processing delays). [P2 W3-5]
- [ ] Add data pipeline observability: task-level logs, metrics, execution history, retries. [P1 W3-4]
- [ ] Add data pipeline testing framework (unit tests for transforms, integration tests for E2E flows). [P1 W3-4]
- [ ] Add idempotency guarantees for pipeline reruns (deduplication, upserts, transaction logs). [P2 W4-6]
- [ ] Add data retention/archival policies per layer (raw → cold storage after N days). [P3 W5+]
- [ ] Add data access audit logs (who accessed which dataset, when, why). [P3 W5+]

## MLOps (Model Lifecycle & Operations)
- [ ] Add ML pipeline CI/CD: automated model training, validation, promotion on code/data changes. [P1 W3-4]
- [ ] Add model versioning and tagging strategy (git SHA, data version, hyperparameters). [P1 W3-4]
- [ ] Add model performance monitoring: accuracy/drift/data quality dashboards in production. [P1 W3-4]
- [ ] Add automated retraining triggers based on drift thresholds or schedule. [P1 W3-4]
- [ ] Add A/B testing framework for model variants (champion/challenger comparison). [P2 W4-6]
- [ ] Add model explainability tooling (SHAP/LIME) for debugging and compliance. [P2 W4-6]
- [ ] Add feature store (Feast/Tecton) for consistent feature serving in training and inference. [P2 W4-6]
- [ ] Add model serving infrastructure (batch predictions + REST API for real-time scoring). [P1 W3-4]
- [ ] Add prediction logging and feedback loop (store predictions, actuals, retrain). [P2 W4-6]
- [ ] Add model rollback mechanism and canary deployment for risky model updates. [P2 W4-6]
- [ ] Add automated hyperparameter tuning pipeline (Optuna/Ray Tune). [P2 W4-6]
- [ ] Add model governance: approval workflow, model card documentation, lineage. [P3 W5+]
- [ ] Add cost monitoring for training/inference infrastructure. [P3 W5+]

## Data Engineering (Pipelines & Infrastructure)
- [ ] Add incremental/delta processing for large datasets (avoid full reprocessing). [P1 W3-4]
- [ ] Add partitioning strategy (by date/region/entity) for optimized query performance. [P1 W3-4]
- [ ] Add data compression and file format optimization (Parquet/ORC over CSV). [P2 W3-5]
- [ ] Add data deduplication logic at ingestion and transformation stages. [P2 W3-5]
- [ ] Add slowly changing dimension (SCD) handling for dimensional data. [P2 W4-6]
- [ ] Add CDC (Change Data Capture) pipeline for database sources. [P2 W4-6]
- [ ] Add data streaming pipelines (Kafka/Kinesis) for real-time ingestion and processing. [P3 W5+]
- [ ] Add data transformation testing (unit tests for SQL/PySpark logic, sample data fixtures). [P1 W3-4]
- [ ] Add data pipeline dependency management (upstream/downstream tracking). [P2 W3-5]
- [ ] Add late-arriving data handling strategy (backfill, merge, alert). [P2 W4-6]
- [ ] Add multi-source data integration with schema mapping and conflict resolution. [P2 W4-6]
- [ ] Add data sampling/subsetting utilities for dev/test environments. [P2 W3-5]
- [ ] Add data masking/anonymization for PII in non-prod environments. [P3 W4-6]
- [ ] Add performance benchmarking for pipeline runtimes and resource usage. [P2 W4-6]

## Data Science (Experimentation & Development)
- [ ] Add experiment tracking workspace (MLflow/W&B) with notebook integration. [P1 W3-4]
- [ ] Add feature engineering library/utilities (shared transforms, encoders, scalers). [P1 W3-4]
- [ ] Add automated feature selection and importance analysis. [P2 W4-6]
- [ ] Add model comparison framework (accuracy, latency, cost across algorithms). [P2 W4-6]
- [ ] Add cross-validation and time-series splitting utilities for robust evaluation. [P2 W4-6]
- [ ] Add notebook templates and best practices (structure, documentation, reproducibility). [P2 W3-5]
- [ ] Add data exploration dashboards (distribution, correlation, missing values). [P2 W3-5]
- [ ] Add statistical testing utilities (hypothesis tests, A/B test analysis). [P2 W4-6]
- [ ] Add causal inference tooling for impact analysis. [P3 W5+]
- [ ] Add synthetic data generation for testing and augmentation. [P3 W5+]
- [ ] Add model interpretation reports (feature contributions, prediction explanations). [P2 W4-6]
- [ ] Add bias/fairness analysis for model predictions. [P3 W5+]

## Data Analysis & BI (Reporting & Insights)
- [ ] Add BI tool integration (Metabase/Superset/Tableau) with data source connectors. [P2 W4-6]
- [ ] Add semantic layer/metrics definitions for consistent reporting. [P2 W4-6]
- [ ] Add automated reporting pipeline for daily/weekly business metrics. [P2 W4-6]
- [ ] Add data visualization library (Plotly/Altair) for exploratory and production dashboards. [P2 W3-5]
- [ ] Add SQL query templates and common analysis patterns documentation. [P2 W3-5]
- [ ] Add data refresh scheduling for BI dashboards and reports. [P2 W4-6]
- [ ] Add alerting for business metric thresholds (revenue drop, anomaly detection). [P2 W4-6]
- [ ] Add user-facing analytics API for embedded dashboards. [P3 W5+]
- [ ] Add self-service data access layer (query builder, data dictionary). [P3 W5+]
- [ ] Add report versioning and change tracking for audit. [P3 W5+]

## Architecture Decisions
- [ ] Document API strategy and defaults: REST for web/mobile, GraphQL for complex UIs, gRPC for microservices. [P3 W5+]
- [ ] Document load balancing approach explicitly covering vertical vs. horizontal scaling. [P3 W5+]
- [ ] Package the service for PyPI (internal or public) with versioning and publish workflow. [P3 W5+]
- [ ] Evaluate a lightweight Heroku deployment path (Herokuapp) for quick demos. [P3 W5+]

## Modular Monolith Design & Service Extraction
- [ ] Define module boundaries for DEX: API layer, data pipelines, model serving, feature engineering, orchestration. [P1 W2-3]
- [ ] Implement clear separation of concerns with independent packages under `src/` (API, core, pipelines, ml). [P1 W2-3]
- [ ] Add internal module interfaces/contracts (protocols/abstract base classes) to minimize coupling. [P1 W2-3]
- [ ] Document shared data layer strategy (database, object storage, cache) accessible by all modules. [P1 W2-3]
- [ ] Add module-level testing: each module testable in isolation with mocked dependencies. [P1 W2-3]
- [ ] Create dependency map showing module relationships and data flow. [P2 W3-4]
- [ ] Define service extraction criteria: independent scaling needs, team ownership, polyglot requirements, async workflows. [P2 W3-4]
- [ ] Identify first service extraction candidate: model serving API (CPU/GPU scaling independent from data pipelines). [P2 W3-5]
- [ ] Design service interface contracts (API spec, event schemas, SLAs) for future extraction. [P2 W3-5]
- [ ] Add API versioning strategy to support gradual service extraction without breaking changes. [P2 W3-5]
- [ ] Document when to extract services vs. keep monolithic (team size, deployment frequency, coupling). [P2 W3-4]
- [ ] Plan event-driven communication layer (Kafka/SQS) for async service interactions (avoid synchronous coupling). [P3 W5+]
- [ ] Create service extraction playbook: steps, testing strategy, rollback plan, monitoring. [P3 W5+]

## Tooling / Backlog
- [ ] Evaluate and, if useful, adopt collaboration/diagramming tools (Miro, Mermaid, Excalidraw). [P3 W5+]
- [ ] Explore OSS components: Minio (object storage), Metabase (BI), Apache Doris (analytics DB), Apache Hop (ETL). [P3 W5+]

## Future Research & Exploration
- [ ] Research microservices architecture patterns for data/ML applications (service mesh, API gateway, distributed tracing). [P3 W5+]
- [ ] Evaluate microservices trade-offs: operational complexity vs. independent scaling, team autonomy, technology diversity. [P3 W5+]
- [ ] Study reference architectures: Netflix (ML inference), Uber (real-time ML), Airbnb (data platform microservices). [P3 W5+]
- [ ] Explore service mesh technologies (Istio, Linkerd) for microservices observability and traffic management. [P3 W5+]
- [ ] Research distributed data management patterns: saga pattern, event sourcing, CQRS for microservices. [P3 W5+]
- [ ] Evaluate serverless ML serving (AWS Lambda, Google Cloud Run) vs. containerized microservices. [P3 W5+]
- [ ] Study cost optimization strategies for microservices: right-sizing, spot instances, auto-scaling policies. [P3 W5+]

