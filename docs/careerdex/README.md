# CareerDEX Project Documentation

**AI-powered career intelligence platform**

## Overview

CareerDEX is an intelligent job matching platform built on the DEX framework. It combines real-time job ingestion, resume analysis, and ML-powered matching to help job seekers find their perfect role.

**Status**: Active development

## 📚 Documentation

- **[CareerDEX Source README](../../src/careerdex/README.md)** - Full package architecture and implementation details
- **[CI/CD Pipeline](../CI_CD.md)** - Packaging, release, and promotion flow

## Implementation

### Current Status

Core package structure implemented with phased modules under `src/careerdex/phases/`.

### Key Components

- **Data Ingestion**: 4-source job fetcher (LinkedIn, Indeed, Glassdoor, Company Pages) - 3-hour cycles
- **Storage**: Medallion architecture (Bronze/Silver/Gold layers)
- **ML Models**: Resume scoring, job matching, salary prediction
- **API**: FastAPI endpoints for job search, matching, recommendations
- **UI**: Web interface for job seekers

## Quick Links

- **GitHub Issues**: [CareerDEX Issues](https://github.com/data-literate/DEX/issues?q=label%3Acareerdex)
- **Main Issues**:
  - Issues #65-71: Development phases
  - Issue #64: Main epic tracking
- **Slack**: #careerdex-dev channel

## Getting Started

1. Read [DEVELOPMENT.md](../DEVELOPMENT.md) to set up local environment
2. Review [CareerDEX Source README](../../src/careerdex/README.md) for architecture
3. Review package release setup in [packages/README.md](../../packages/README.md)

## Directory Structure

```
src/careerdex/
├── dags/
│   └── job_ingestion_dag.py         # Airflow DAG (10 tasks)
├── core/
│   └── notifier.py                  # Slack notifications
├── models/
│   └── [ML models]
├── phases/
│   └── phase1-6 implementations
└── README.md
```

---

**Documentation Hub**: [See docs/README.md](../README.md)
