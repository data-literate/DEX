"""
dex-data — Data connectors, profiling, and schema registry (Epic #37).

Provides:
    - Abstract ``DataConnector`` interface and concrete REST/file connectors
    - ``DataProfiler`` for automated dataset statistics
    - ``SchemaRegistry`` for versioned schema management
"""

from .connectors import DataConnector, FileConnector, RestConnector
from .profiler import DataProfiler, ProfileReport
from .registry import SchemaRegistry, SchemaVersion

__all__ = [
    "DataConnector",
    "FileConnector",
    "ProfileReport",
    "DataProfiler",
    "RestConnector",
    "SchemaRegistry",
    "SchemaVersion",
]
