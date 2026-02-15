# CareerDEX Project Documentation

**AI-powered career intelligence platform**

## Overview

CareerDEX is an intelligent job matching platform built on the DEX framework. It combines real-time job ingestion, resume analysis, and ML-powered matching to help job seekers find their perfect role.

**Status**: Development Ready (v0.3.0)  
**Release Target**: End of February 2026

## 📚 Documentation

- **[CareerDEX Complete Guide](../CAREERDEX_V0.3.0_COMPLETE.md)** - Full specification, architecture, and implementation timeline
- **[Notifications Setup](../../src/careerdex/NOTIFICATIONS_SETUP.md)** - Slack webhook configuration
- **[Modernization Summary](../../src/careerdex/MODERNIZATION_SUMMARY.md)** - Framework migration notes

## Implementation

### Current Status

Phase 1 Foundation (v0.3.1) - In Progress

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

1. Read [DEVELOPMENT.md](../common/DEVELOPMENT.md) to set up local environment
2. Review [CareerDEX Complete Guide](../CAREERDEX_V0.3.0_COMPLETE.md) for architecture
3. Check [Notifications Setup](../../src/careerdex/NOTIFICATIONS_SETUP.md) for monitoring

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
