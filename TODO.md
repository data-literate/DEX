# TODO

## Vision Alignment

DEX is an end‑to‑end framework that unifies data engineering, lakehouse warehousing, MLOps, AI serving, and DevOps. This backlog is organized by portfolio modules and platform enablers to keep execution aligned with that vision.

---

## Completed ✅

### Platform Foundations
- ✅ GitHub Actions CI pipeline (lint, tests, build, push)
- ✅ Docker image build and push to ghcr.io
- ✅ Security scanning (CodeQL, Trivy)
- ✅ ArgoCD GitOps with multi‑environment deployment
- ✅ Kustomize overlays (dev/stage/prod/preview)
- ✅ CD workflow with manifest updates
- ✅ Structured logging + Prometheus metrics + OpenTelemetry tracing

---

## Now (v0.2.0 – Production Hardening)

### Core API & Reliability
- [ ] Enhanced health/readiness/startup probes
- [ ] E2E API tests
- [ ] Request validation and error handling

### Observability & Ops
- [ ] Dashboards for metrics/logs/traces (Grafana/Loki/Tempo)
- [ ] Alerting rules tied to SLOs

### Dev Experience
- [ ] Clean API examples

---

## Next (v0.3.0 – Data Platform)

- [ ] Data quality framework (schema + expectations)
- [ ] Orchestration with Airflow/Dagster
- [ ] Storage layers (raw/bronze/silver/gold)
- [ ] Weather pipeline E2E + lineage

---

## DEX Portfolio Modules (Roadmap)

### dex-data (Engineering)
- [ ] Spark batch pipelines with partitioning + incremental loads
- [ ] Kafka streaming pipeline with schema validation and DLQ
- [ ] Orchestration patterns (retry/backfill)

### dex-warehouse (Warehousing)
- [ ] dbt staging → marts models
- [ ] ML‑ready feature tables
- [ ] Incremental models + tests (unique/not_null)

### dex-lakehouse (Storage)
- [ ] Iceberg/Delta datasets (Parquet/Avro)
- [ ] Bronze/silver/gold demos
- [ ] Snapshot + time‑travel examples

### dex-ml (MLOps)
- [ ] MLflow tracking + model registry
- [ ] Feature store integration (Feast/Tecton)
- [ ] Model serving (batch + real‑time)
- [ ] RAG/Vector DB example (Pinecone)

### dex-api (Serving)
- [ ] Feature retrieval APIs
- [ ] Model inference APIs
- [ ] AuthN/AuthZ (OIDC/JWT)

### dex-ops (DevOps)
- [ ] Terraform IaC for AWS/GCP
- [ ] Kubernetes templates (Helm/Kustomize)
- [ ] Secrets management + zero‑trust IAM

---

## Platform Enablers (Cross‑Cutting)

### Security & Compliance
- [ ] Hardened security headers (CSP/HSTS)
- [ ] Dependency scanning automation (Dependabot/Renovate)

### Resilience & Scale
- [ ] Caching layer (Redis) + rate limiting
- [ ] Blue/green or canary deployment strategy
- [ ] Disaster recovery (RTO/RPO + backups)

### Governance
- [ ] Data catalog/lineage tool (OpenMetadata/Amundsen)
- [ ] Model monitoring for drift + performance

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

