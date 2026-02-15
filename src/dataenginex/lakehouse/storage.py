"""
Concrete storage backends for the DEX lakehouse.

Both ``ParquetStorage`` and ``JsonStorage`` implement the
``StorageBackend`` ABC from ``dataenginex.core.medallion_architecture`` so
they can be used interchangeably by the ``DualStorage`` layer.

``ParquetStorage`` delegates to *pyarrow* when available; otherwise it
falls back to ``JsonStorage`` with a logged warning.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from dataenginex.core.medallion_architecture import StorageBackend, StorageFormat

logger = logging.getLogger(__name__)

# Try importing pyarrow — optional heavyweight dependency
try:
    import pyarrow as pa  # type: ignore[import-not-found]
    import pyarrow.parquet as pq  # type: ignore[import-not-found]

    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False


# ---------------------------------------------------------------------------
# JSON storage (always available)
# ---------------------------------------------------------------------------

class JsonStorage(StorageBackend):
    """Simple JSON-file storage for development and testing.

    Each ``write`` call serialises *data* (list of dicts) as a JSON array.
    """

    def __init__(self, base_path: str = "data") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("JsonStorage initialised at %s", self.base_path)

    def write(
        self,
        data: Any,
        path: str,
        format: StorageFormat = StorageFormat.PARQUET,
    ) -> bool:
        try:
            full = self.base_path / f"{path}.json"
            full.parent.mkdir(parents=True, exist_ok=True)
            records = self._normalise(data)
            full.write_text(json.dumps(records, indent=2, default=str))
            logger.info("Wrote %d records to %s", len(records), full)
            return True
        except Exception as exc:
            logger.error("JsonStorage write failed: %s", exc)
            return False

    def read(self, path: str, format: StorageFormat = StorageFormat.PARQUET) -> Any:
        try:
            full = self.base_path / f"{path}.json"
            if not full.exists():
                logger.warning("File not found: %s", full)
                return None
            return json.loads(full.read_text())
        except Exception as exc:
            logger.error("JsonStorage read failed: %s", exc)
            return None

    def delete(self, path: str) -> bool:
        try:
            full = self.base_path / f"{path}.json"
            if full.exists():
                full.unlink()
                logger.info("Deleted %s", full)
            return True
        except Exception as exc:
            logger.error("JsonStorage delete failed: %s", exc)
            return False

    @staticmethod
    def _normalise(data: Any) -> list[dict[str, Any]]:
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
        return [{"value": data}]


# ---------------------------------------------------------------------------
# Parquet storage (requires pyarrow)
# ---------------------------------------------------------------------------

class ParquetStorage(StorageBackend):
    """Parquet file storage backed by *pyarrow*.

    Falls back to ``JsonStorage`` when *pyarrow* is not installed.
    """

    def __init__(self, base_path: str = "data", compression: str = "snappy") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.compression = compression

        if _HAS_PYARROW:
            logger.info("ParquetStorage initialised at %s (pyarrow available)", self.base_path)
        else:
            logger.warning(
                "pyarrow not installed — ParquetStorage will use JSON fallback"
            )
            self._fallback = JsonStorage(str(self.base_path))

    def write(
        self,
        data: Any,
        path: str,
        format: StorageFormat = StorageFormat.PARQUET,
    ) -> bool:
        if not _HAS_PYARROW:
            return self._fallback.write(data, path, format)

        try:
            full = self.base_path / f"{path}.parquet"
            full.parent.mkdir(parents=True, exist_ok=True)
            records = self._to_records(data)
            if not records:
                logger.warning("No records to write to %s", full)
                return False
            table = pa.Table.from_pylist(records)
            pq.write_table(table, str(full), compression=self.compression)
            logger.info("Wrote %d records to %s", len(records), full)
            return True
        except Exception as exc:
            logger.error("ParquetStorage write failed: %s", exc)
            return False

    def read(self, path: str, format: StorageFormat = StorageFormat.PARQUET) -> Any:
        if not _HAS_PYARROW:
            return self._fallback.read(path, format)

        try:
            full = self.base_path / f"{path}.parquet"
            if not full.exists():
                logger.warning("Parquet file not found: %s", full)
                return None
            table = pq.read_table(str(full))
            return table.to_pylist()
        except Exception as exc:
            logger.error("ParquetStorage read failed: %s", exc)
            return None

    def delete(self, path: str) -> bool:
        if not _HAS_PYARROW:
            return self._fallback.delete(path)

        try:
            full = self.base_path / f"{path}.parquet"
            if full.exists():
                full.unlink()
                logger.info("Deleted %s", full)
            return True
        except Exception as exc:
            logger.error("ParquetStorage delete failed: %s", exc)
            return False

    @staticmethod
    def _to_records(data: Any) -> list[dict[str, Any]]:
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
        return []
