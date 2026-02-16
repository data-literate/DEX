"""
dex-lakehouse — Storage backends, data catalog, and partitioning (Epic #39).

Provides:
    - ``ParquetStorage`` / ``JsonStorage`` — concrete ``StorageBackend`` impls
    - ``DataCatalog`` — registry of datasets with metadata
    - ``PartitionStrategy`` — time/hash/range-based partitioning helpers
"""

from .catalog import CatalogEntry, DataCatalog
from .partitioning import DatePartitioner, HashPartitioner, PartitionStrategy
from .storage import JsonStorage, ParquetStorage

__all__ = [
    "CatalogEntry",
    "DataCatalog",
    "DatePartitioner",
    "HashPartitioner",
    "JsonStorage",
    "ParquetStorage",
    "PartitionStrategy",
]
