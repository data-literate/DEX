# Changelog

All notable changes to `dataenginex` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.8] - 2026-02-21

### Added

- PySpark local-mode test fixtures in `tests/conftest.py` (session-scoped `spark` session)
- Sample DataFrame fixtures: `spark_df_jobs`, `spark_df_weather`, `spark_df_empty`
- `requires_pyspark` skip marker — tests auto-skip when PySpark is not installed
- `tests/fixtures/sample_data.py` — factory helpers for job, user, and weather records
- `tests/unit/test_spark_fixtures.py` — validates PySpark fixture behaviour

## [0.4.6] - 2026-02-21

### Added

- `QualityGate` — orchestrates quality checks at medallion layer transitions
- `QualityStore` — in-memory store accumulating per-layer quality metrics
- `QualityResult` — immutable dataclass capturing evaluation outcomes
- `QualityDimension` — StrEnum for named quality dimensions
- `/api/v1/data/quality/{layer}` endpoint for per-layer quality history
- `set_quality_store()` / `get_quality_store()` for wiring quality at app startup
- New exports in `dataenginex.core` and `dataenginex.api`

### Changed

- `/api/v1/data/quality` now returns live metrics from `QualityStore` (was placeholder zeros)
- Wired `DataProfiler`, `DataQualityChecks`, and `QualityScorer` into `QualityGate` pipeline

## [0.4.5] - 2026-02-21

### Added

- `StorageBackend` ABC with proper `@abstractmethod` contracts
- `S3Storage` backend for AWS S3 (requires `boto3`)
- `GCSStorage` backend for Google Cloud Storage (requires `google-cloud-storage`)
- Re-exported `StorageBackend` from `dataenginex.lakehouse`

### Changed

- Refactored `StorageBackend` from plain class to proper `ABC` subclass
- Updated `lakehouse.__init__` to export all 4 storage backends + ABC

## [0.4.3] - 2026-02-21

### Added

- Comprehensive attribute-level docstrings on all public dataclasses
- `from __future__ import annotations` in all source modules
- Module-level class/function inventory docstrings
- mkdocs API reference configuration with `mkdocstrings` plugin
- API reference pages for all 7 subpackages under `docs/api-reference/`

### Changed

- Upgraded mkdocs theme from `mkdocs` to `material`
- Enhanced module docstrings in middleware, core, and validators

## [0.4.1] - 2026-02-21

### Added

- CHANGELOG.md with Keep a Changelog format
- Release workflow extracts changelog notes for GitHub Releases automatically

### Changed

- `release.yml` now reads `packages/dataenginex/CHANGELOG.md` for release notes

## [0.4.0] - 2026-02-21

### Added

- Stable `__all__` exports in every subpackage `__init__.py`
- `from __future__ import annotations` in all public modules
- Comprehensive module-level docstrings with usage examples
- New public API exports: `ComponentHealth`, `AuthMiddleware`, `AuthUser`,
  `create_token`, `decode_token`, `BadRequestError`, `NotFoundError`,
  `PaginationMeta`, `RateLimiter`, `RateLimitMiddleware`,
  `ConnectorStatus`, `FetchResult`, `ColumnProfile`, `get_logger`, `get_tracer`

### Changed

- Reorganized `__all__` in all subpackages for logical grouping
- Updated package version to 0.4.0

## [0.3.5] - 2026-02-13

### Added

- Production hardening: structured logging, Prometheus/OTel, health probes
- Data connectors: `RestConnector`, `FileConnector` with async interface
- Schema registry with versioned schema management
- Data profiler with automated dataset statistics
- Lakehouse catalog, partitioning, and storage backends
- ML framework: trainer, model registry, drift detection, serving
- Warehouse transforms and persistent lineage tracking
- JWT authentication middleware
- Rate limiting middleware
- Cursor-based pagination utilities
- Versioned API router (`/api/v1/`)

[Unreleased]: https://github.com/TheDataEngineX/DEX/compare/v0.4.8...HEAD
[0.4.8]: https://github.com/TheDataEngineX/DEX/compare/v0.4.6...v0.4.8
[0.4.6]: https://github.com/TheDataEngineX/DEX/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/TheDataEngineX/DEX/compare/v0.4.3...v0.4.5
[0.4.3]: https://github.com/TheDataEngineX/DEX/compare/v0.4.1...v0.4.3
[0.4.1]: https://github.com/TheDataEngineX/DEX/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/TheDataEngineX/DEX/compare/v0.3.5...v0.4.0
[0.3.5]: https://github.com/TheDataEngineX/DEX/releases/tag/v0.3.5
