# dataenginex

`dataenginex` is the core DataEngineX framework package for building observable, production-ready data and API services.

It provides:
- FastAPI application primitives and API extensions
- Middleware for structured logging, metrics, and tracing
- Data quality and validation utilities
- Lakehouse and warehouse building blocks
- Reusable ML support modules for model-serving workflows

## Install

```bash
pip install dataenginex
```

## Package Scope

This package is the core library from the DEX monorepo.
`careerdex` and `weatherdex` are maintained in the same repository but are not part of this package release flow.

## Quick Usage

```python
from dataenginex import __version__

print(__version__)
```

## Source and Docs

- Repository: https://github.com/TheDataEngineX/DEX
- CI/CD guide: `docs/CI_CD.md`
- Release notes: `packages/dataenginex/src/dataenginex/RELEASE_NOTES.md`
