"""
dex-warehouse — SQL-like transforms, persistent lineage, warehouse utilities (Epic #38).

Provides:
    - ``Transform`` / ``TransformPipeline`` for declarative data transforms
    - ``PersistentLineage`` for JSON-backed data lineage tracking
    - ``WarehouseManager`` for coordinating medallion layer writes
"""

from .lineage import LineageEvent, PersistentLineage
from .transforms import Transform, TransformPipeline, TransformResult

__all__ = [
    "LineageEvent",
    "PersistentLineage",
    "Transform",
    "TransformPipeline",
    "TransformResult",
]
