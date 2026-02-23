"""
DataEngineX (DEX) — Core framework for data engineering projects.

Public API surface. Import from top-level or from subpackages:

    from dataenginex import __version__
    from dataenginex.api import HealthChecker, HealthStatus
    from dataenginex.core import MedallionArchitecture, DataLayer
    from dataenginex.data import DataConnector, DataProfiler, SchemaRegistry
    from dataenginex.lakehouse import DataCatalog, ParquetStorage
    from dataenginex.middleware import configure_logging, configure_tracing
    from dataenginex.ml import ModelRegistry, SklearnTrainer, DriftDetector
    from dataenginex.warehouse import PersistentLineage, TransformPipeline

Submodules:
    api        – FastAPI application, health checks, error handling, pagination
    core       – Schemas, validators, medallion architecture, pipeline config
    data       – Data connectors, profiler, schema registry
    lakehouse  – Storage backends, data catalog, partitioning
    middleware – Logging, metrics, tracing, request middleware
    ml         – ML training, model registry, drift detection, serving
    warehouse  – Transforms, persistent lineage tracking
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("dataenginex")
except PackageNotFoundError:
    __version__ = "0.4.0"

__all__ = ["__version__"]
