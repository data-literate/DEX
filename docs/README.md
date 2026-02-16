# DEX Documentation Hub

**All documentation organized by topic and project.**

---

## Getting Started

**New to DEX? Start here:**
1. **[Main README](../Readme.md)** - Project overview
2. **[Development Setup](./common/DEVELOPMENT.md)** - Local environment setup
3. **[Setup Verification](./common/SETUP_COMPLETE.md)** - Verify your installation
4. **[Contributing](./common/CONTRIBUTING.md)** - How to contribute

---

## 📂 Documentation Structure

### Framework (Common)

Core documentation for all DEX developers:

- **[Development Setup](./common/DEVELOPMENT.md)** - Local development, workflow, testing
- **[Contributing Guidelines](./common/CONTRIBUTING.md)** - Code style, commits, PR process
- **[Setup Verification](./common/SETUP_COMPLETE.md)** - Checklist to verify setup is complete
- **[Architecture](./common/ARCHITECTURE.md)** - System design and technology stack
- **[Architecture Decision Records (ADRs)](./adr/)** - Rationale for major technical decisions
  - [ADR-0001: Medallion Architecture](./adr/0001-medallion-architecture.md)
- **[CI/CD Pipeline](./common/CI_CD.md)** - GitHub Actions automation
- **[Deployment Runbook](./common/DEPLOY_RUNBOOK.md)** - Release procedures
- **[Observability](./common/OBSERVABILITY.md)** - Monitoring, logging, tracing
- **[Project Management](./common/PROJECT_MANAGEMENT.md)** - GitHub workflow
- **[SDLC](./common/SDLC.md)** - Software development lifecycle
- **[Project Board Setup](./common/PROJECT_BOARD_SETUP.md)** - GitHub Project Board config
- **[Release Notes](./common/RELEASE_NOTES.md)** - Version history
- **[Kubernetes Setup](./common/LOCAL_K8S_SETUP.md)** - Local K8s configuration

### Projects

Project-specific documentation:

**CareerDEX** (v0.3.0 - Job Intelligence Platform)
- **[CareerDEX Complete Guide](./careerdex/CAREERDEX_V0.3.0_COMPLETE.md)** - Full spec and architecture
- **[Notifications Setup](../src/careerdex/NOTIFICATIONS_SETUP.md)** - Slack integration
- **[Modernization Summary](../src/careerdex/MODERNIZATION_SUMMARY.md)** - Framework migration

**Weather** (Reference Implementation)
- **[Weather Pipeline](../src/weatherdex/START_HERE.md)** - Quick start guide
- **[ML Implementation](../src/weatherdex/ML_README.md)** - ML models and training

### Planning

- **[Project Roadmap](./roadmap/project-roadmap.json)** - Strategic milestones
- **[GitHub Issues](https://github.com/data-literate/DEX/issues)** - Task tracking

---

## 🔍 Find What You Need

| Task | Link |
|------|------|
| Set up local development | [Development Setup](./common/DEVELOPMENT.md) |
| Understand the architecture | [Architecture](./common/ARCHITECTURE.md) |
| Deploy to production | [Deployment Runbook](./common/DEPLOY_RUNBOOK.md) |
| Set up monitoring | [Observability](./common/OBSERVABILITY.md) |
| Contribute code | [Contributing](./common/CONTRIBUTING.md) |
| Understand CI/CD | [CI/CD Pipeline](./common/CI_CD.md) |
| Track work | [Project Management](./common/PROJECT_MANAGEMENT.md) |
| Work on CareerDEX | [CareerDEX Guide](./careerdex/CAREERDEX_V0.3.0_COMPLETE.md) |
| Learn from reference | [Weather Pipeline](../src/weatherdex/START_HERE.md) |

---

## Documentation Structure

```
docs/
├── README.md (this file)
├── common/                     # Framework-wide docs
│   ├── DEVELOPMENT.md
│   ├── CONTRIBUTING.md
│   ├── SETUP_COMPLETE.md
│   ├── ARCHITECTURE.md
│   ├── CI_CD.md
│   ├── DEPLOY_RUNBOOK.md
│   ├── OBSERVABILITY.md
│   ├── PROJECT_MANAGEMENT.md
│   ├── SDLC.md
│   ├── PROJECT_BOARD_SETUP.md
│   ├── RELEASE_NOTES.md
│   └── LOCAL_K8S_SETUP.md
├── adr/                        # Architecture decisions
│   ├── 0000-template.md
│   ├── 0001-medallion-architecture.md
│   └── ...
├── careerdex/                  # CareerDEX project
│   └── CAREERDEX_V0.3.0_COMPLETE.md
├── weather/                    # Weather reference
│   └── (see ../src/weatherdex/)
├── roadmap/                    # Strategic planning
│   ├── project-roadmap.json
│   └── project-roadmap.csv
└── (other docs organized by topic)
```

---

**Last Updated:** February 15, 2026 | **Version:** v0.2.0-dev
