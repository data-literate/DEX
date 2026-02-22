"""Storage backends, data catalog, and partitioning.

Public API::

    from dataenginex.lakehouse import (
        ParquetStorage, JsonStorage,
        CatalogEntry, DataCatalog,
        PartitionStrategy, DatePartitioner, HashPartitioner,
    )
"""

from __future__ import annotations

from .catalog import CatalogEntry, DataCatalog
from .partitioning import DatePartitioner, HashPartitioner, PartitionStrategy
from .storage import JsonStorage, ParquetStorage

__all__ = [
    # Catalog
    "CatalogEntry",
    "DataCatalog",
    # Partitioning
    "DatePartitioner",
    "HashPartitioner",
    "PartitionStrategy",
    # Storage
    "JsonStorage",
    "ParquetStorage",
]
