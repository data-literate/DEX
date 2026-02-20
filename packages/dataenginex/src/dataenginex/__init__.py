"""
DataEngineX (DEX) — Core framework for data engineering projects.

Submodules:
    api        – FastAPI application, health checks, error handling
    core       – Schemas, validators, medallion architecture, pipeline config
    middleware – Logging, metrics, tracing, request middleware
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("dataenginex")
except PackageNotFoundError:
    __version__ = "0.3.5"

