"""
Concrete storage backends for the DEX lakehouse.

``JsonStorage``, ``ParquetStorage``, ``S3Storage``, and ``GCSStorage``
implement the ``StorageBackend`` ABC from
``dataenginex.core.medallion_architecture`` so they can be used
interchangeably by the ``DualStorage`` layer.

``ParquetStorage`` delegates to *pyarrow* when available; otherwise it
falls back to ``JsonStorage`` with a logged warning.

``S3Storage`` and ``GCSStorage`` are stub implementations that log
operations but require ``boto3`` / ``google-cloud-storage`` at runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger

from dataenginex.core.medallion_architecture import StorageBackend, StorageFormat

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
            logger.warning("pyarrow not installed — ParquetStorage will use JSON fallback")
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


# ---------------------------------------------------------------------------
# S3 storage (requires boto3)
# ---------------------------------------------------------------------------

try:
    import boto3  # type: ignore[import-not-found]

    _HAS_BOTO3 = True
except ImportError:
    _HAS_BOTO3 = False


class S3Storage(StorageBackend):
    """AWS S3 object storage backend.

    Reads/writes JSON-serialised records to an S3 bucket.  Requires
    ``boto3`` at runtime.

    Parameters
    ----------
    bucket:
        S3 bucket name.
    prefix:
        Key prefix for all objects (default ``""``).
    region:
        AWS region (default ``"us-east-1"``).
    """

    def __init__(
        self,
        bucket: str,
        prefix: str = "",
        region: str = "us-east-1",
    ) -> None:
        self.bucket = bucket
        self.prefix = prefix.rstrip("/")
        self.region = region

        if not _HAS_BOTO3:
            logger.warning("boto3 not installed — S3Storage operations will fail")
            self._client = None
        else:
            self._client = boto3.client("s3", region_name=region)
            logger.info("S3Storage initialised: s3://%s/%s", bucket, prefix)

    def _key(self, path: str) -> str:
        return f"{self.prefix}/{path}" if self.prefix else path

    def write(
        self,
        data: Any,
        path: str,
        format: StorageFormat = StorageFormat.PARQUET,
    ) -> bool:
        """Write JSON-serialised data to S3."""
        if self._client is None:
            logger.error("S3Storage: boto3 not available")
            return False
        try:
            records = data if isinstance(data, list) else [data]
            body = json.dumps(records, default=str).encode()
            key = self._key(f"{path}.json")
            self._client.put_object(Bucket=self.bucket, Key=key, Body=body)
            logger.info("Wrote %d records to s3://%s/%s", len(records), self.bucket, key)
            return True
        except Exception as exc:
            logger.error("S3Storage write failed: %s", exc)
            return False

    def read(self, path: str, format: StorageFormat = StorageFormat.PARQUET) -> Any:
        """Read JSON data from S3."""
        if self._client is None:
            logger.error("S3Storage: boto3 not available")
            return None
        try:
            key = self._key(f"{path}.json")
            response = self._client.get_object(Bucket=self.bucket, Key=key)
            body = response["Body"].read().decode()
            return json.loads(body)
        except Exception as exc:
            logger.error("S3Storage read failed: %s", exc)
            return None

    def delete(self, path: str) -> bool:
        """Delete object from S3."""
        if self._client is None:
            logger.error("S3Storage: boto3 not available")
            return False
        try:
            key = self._key(f"{path}.json")
            self._client.delete_object(Bucket=self.bucket, Key=key)
            logger.info("Deleted s3://%s/%s", self.bucket, key)
            return True
        except Exception as exc:
            logger.error("S3Storage delete failed: %s", exc)
            return False


# ---------------------------------------------------------------------------
# GCS storage (requires google-cloud-storage)
# ---------------------------------------------------------------------------

try:
    from google.cloud import storage as gcs_storage  # type: ignore[import-untyped]

    _HAS_GCS = True
except ImportError:
    _HAS_GCS = False


class GCSStorage(StorageBackend):
    """Google Cloud Storage backend.

    Reads/writes JSON-serialised records to a GCS bucket.  Requires
    ``google-cloud-storage`` at runtime.

    Parameters
    ----------
    bucket:
        GCS bucket name.
    prefix:
        Key prefix for all objects (default ``""``).
    project:
        GCP project ID (optional, uses ADC default).
    """

    def __init__(
        self,
        bucket: str,
        prefix: str = "",
        project: str | None = None,
    ) -> None:
        self.bucket_name = bucket
        self.prefix = prefix.rstrip("/")

        if not _HAS_GCS:
            logger.warning("google-cloud-storage not installed — GCSStorage operations will fail")
            self._bucket = None
        else:
            client = gcs_storage.Client(project=project)
            self._bucket = client.bucket(bucket)
            logger.info("GCSStorage initialised: gs://%s/%s", bucket, prefix)

    def _blob_name(self, path: str) -> str:
        return f"{self.prefix}/{path}" if self.prefix else path

    def write(
        self,
        data: Any,
        path: str,
        format: StorageFormat = StorageFormat.PARQUET,
    ) -> bool:
        """Write JSON-serialised data to GCS."""
        if self._bucket is None:
            logger.error("GCSStorage: google-cloud-storage not available")
            return False
        try:
            records = data if isinstance(data, list) else [data]
            body = json.dumps(records, default=str)
            blob = self._bucket.blob(self._blob_name(f"{path}.json"))
            blob.upload_from_string(body, content_type="application/json")
            logger.info(
                "Wrote %d records to gs://%s/%s",
                len(records),
                self.bucket_name,
                blob.name,
            )
            return True
        except Exception as exc:
            logger.error("GCSStorage write failed: %s", exc)
            return False

    def read(self, path: str, format: StorageFormat = StorageFormat.PARQUET) -> Any:
        """Read JSON data from GCS."""
        if self._bucket is None:
            logger.error("GCSStorage: google-cloud-storage not available")
            return None
        try:
            blob = self._bucket.blob(self._blob_name(f"{path}.json"))
            body = blob.download_as_text()
            return json.loads(body)
        except Exception as exc:
            logger.error("GCSStorage read failed: %s", exc)
            return None

    def delete(self, path: str) -> bool:
        """Delete object from GCS."""
        if self._bucket is None:
            logger.error("GCSStorage: google-cloud-storage not available")
            return False
        try:
            blob = self._bucket.blob(self._blob_name(f"{path}.json"))
            blob.delete()
            logger.info("Deleted gs://%s/%s", self.bucket_name, blob.name)
            return True
        except Exception as exc:
            logger.error("GCSStorage delete failed: %s", exc)
            return False
