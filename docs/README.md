# DEX Documentation Hub

**All documentation organized by topic and project.**

---

## Getting Started

**New to DEX? Start here:**
1. **[Main README](../README.md)** - Project overview
2. **[Development Setup](./DEVELOPMENT.md)** - Local environment setup
3. **[CI/CD Pipeline](./CI_CD.md)** - Build, release, and publish workflow
4. **[Contributing](./CONTRIBUTING.md)** - How to contribute

---

## 📂 Documentation Structure

### Framework (Common)

Core documentation for all DEX developers:

- **[Development Setup](./DEVELOPMENT.md)** - Local development, workflow, testing
- **[Contributing Guidelines](./CONTRIBUTING.md)** - Code style, commits, PR process
- **[Architecture](./ARCHITECTURE.md)** - System design and technology stack
- **[Architecture Decision Records (ADRs)](./adr/)** - Rationale for major technical decisions
  - [ADR-0001: Medallion Architecture](./adr/0001-medallion-architecture.md)
- **[CI/CD Pipeline](./CI_CD.md)** - GitHub Actions automation
- **[Deployment Runbook](./DEPLOY_RUNBOOK.md)** - Release procedures
- **[Observability](./OBSERVABILITY.md)** - Monitoring, logging, tracing
- **[SDLC](./SDLC.md)** - Software development lifecycle
- **[Release Notes](./RELEASE_NOTES.md)** - Version history
- **[Kubernetes Setup](./LOCAL_K8S_SETUP.md)** - Local K8s configuration

### Projects

Project-specific documentation:

**CareerDEX**
- **[CareerDEX Docs](./careerdex/README.md)** - Project overview and implementation status
- **[Source Package](../src/careerdex/README.md)** - Package-level structure and architecture

**Weather** (Reference Implementation)
- **[Weather Docs](./weather/README.md)** - Reference implementation guide
- **[Source Package](../src/weatherdex/README.md)** - Source package summary

### Planning

- **[Project Roadmap](./roadmap/project-roadmap.json)** - Strategic milestones
- **[GitHub Issues](https://github.com/TheDataEngineX/DEX/issues)** - Task tracking

---

## 🔍 Find What You Need

| Task | Link |
|------|------|
| Set up local development | [Development Setup](./DEVELOPMENT.md) |
| Understand the architecture | [Architecture](./ARCHITECTURE.md) |
| Deploy to production | [Deployment Runbook](./DEPLOY_RUNBOOK.md) |
| Set up monitoring | [Observability](./OBSERVABILITY.md) |
| Contribute code | [Contributing](./CONTRIBUTING.md) |
| Understand CI/CD | [CI/CD Pipeline](./CI_CD.md) |
| Track work | [SDLC](./SDLC.md) |
| Work on CareerDEX | [CareerDEX Docs](./careerdex/README.md) |
| Learn from reference | [Weather Docs](./weather/README.md) |

---

## Documentation Structure

```
docs/
├── README.md (this file)
├── DEVELOPMENT.md
├── CONTRIBUTING.md
├── ARCHITECTURE.md
├── CI_CD.md
├── DEPLOY_RUNBOOK.md
├── OBSERVABILITY.md
├── SDLC.md
├── RELEASE_NOTES.md
├── LOCAL_K8S_SETUP.md
├── adr/                        # Architecture decisions
│   ├── 0000-template.md
│   ├── 0001-medallion-architecture.md
│   └── ...
├── careerdex/                  # CareerDEX project
│   └── README.md
├── weather/                    # Weather reference
│   └── README.md
├── roadmap/                    # Strategic planning
│   ├── project-roadmap.json
│   └── project-roadmap.csv
└── (other docs organized by topic)
```

---

**Version**: v0.3.5 | **Updated**: Feb 21, 2026
