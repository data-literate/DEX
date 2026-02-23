"""Tests for medallion architecture components."""

from __future__ import annotations

import pytest
from dataenginex.core.medallion_architecture import (
    BigQueryStorage,
    DataLayer,
    DataLineage,
    DualStorage,
    LayerConfiguration,
    LocalParquetStorage,
    MedallionArchitecture,
    StorageFormat,
)

# ---------------------------------------------------------------------------
# LayerConfiguration
# ---------------------------------------------------------------------------


class TestLayerConfiguration:
    def test_valid_construction(self) -> None:
        cfg = LayerConfiguration(
            layer_name="bronze",
            description="raw data",
            purpose="preserve",
            storage_format=StorageFormat.PARQUET,
            local_path="data/bronze",
            bigquery_dataset="ds_bronze",
            retention_days=30,
            schema_validation=False,
            quality_threshold=0.0,
        )
        assert cfg.layer_name == "bronze"
        assert cfg.compression == "snappy"

    def test_invalid_quality_threshold_high(self) -> None:
        with pytest.raises(ValueError, match="quality_threshold"):
            LayerConfiguration(
                layer_name="gold",
                description="d",
                purpose="p",
                storage_format=StorageFormat.PARQUET,
                local_path="data/gold",
                bigquery_dataset="ds_gold",
                retention_days=None,
                schema_validation=True,
                quality_threshold=1.5,
            )

    def test_invalid_quality_threshold_negative(self) -> None:
        with pytest.raises(ValueError, match="quality_threshold"):
            LayerConfiguration(
                layer_name="gold",
                description="d",
                purpose="p",
                storage_format=StorageFormat.PARQUET,
                local_path="data/gold",
                bigquery_dataset="ds_gold",
                retention_days=None,
                schema_validation=True,
                quality_threshold=-0.1,
            )


# ---------------------------------------------------------------------------
# MedallionArchitecture
# ---------------------------------------------------------------------------


class TestMedallionArchitecture:
    def test_get_bronze_config(self) -> None:
        cfg = MedallionArchitecture.get_layer_config(DataLayer.BRONZE)
        assert cfg is not None
        assert cfg.layer_name == "bronze"
        assert cfg.quality_threshold == 0.0

    def test_get_silver_config(self) -> None:
        cfg = MedallionArchitecture.get_layer_config(DataLayer.SILVER)
        assert cfg is not None
        assert cfg.quality_threshold == 0.75

    def test_get_gold_config(self) -> None:
        cfg = MedallionArchitecture.get_layer_config(DataLayer.GOLD)
        assert cfg is not None
        assert cfg.quality_threshold == 0.90

    def test_get_all_layers_returns_three(self) -> None:
        layers = MedallionArchitecture.get_all_layers()
        assert len(layers) == 3
        assert [layer.layer_name for layer in layers] == ["bronze", "silver", "gold"]


# ---------------------------------------------------------------------------
# LocalParquetStorage
# ---------------------------------------------------------------------------


class TestLocalParquetStorage:
    def test_write_success(self) -> None:
        storage = LocalParquetStorage("data")
        assert storage.write({"a": 1}, "test/path") is True

    def test_write_wrong_format(self) -> None:
        storage = LocalParquetStorage("data")
        assert storage.write({"a": 1}, "test/path", StorageFormat.BIGQUERY) is False

    def test_read_returns_none(self) -> None:
        storage = LocalParquetStorage("data")
        result = storage.read("test/path")
        assert result is None

    def test_delete_success(self) -> None:
        storage = LocalParquetStorage("data")
        assert storage.delete("test/path") is True


# ---------------------------------------------------------------------------
# BigQueryStorage
# ---------------------------------------------------------------------------


class TestBigQueryStorage:
    def test_write_success(self) -> None:
        storage = BigQueryStorage("my-project")
        assert storage.write({"a": 1}, "ds.table") is True

    def test_write_wrong_format(self) -> None:
        storage = BigQueryStorage("my-project")
        assert storage.write({"a": 1}, "ds.table", StorageFormat.PARQUET) is False

    def test_read_returns_none(self) -> None:
        storage = BigQueryStorage("my-project")
        result = storage.read("ds.table")
        assert result is None

    def test_delete_success(self) -> None:
        storage = BigQueryStorage("my-project")
        assert storage.delete("ds.table") is True


# ---------------------------------------------------------------------------
# DualStorage
# ---------------------------------------------------------------------------


class TestDualStorage:
    def test_local_only_write_bronze(self) -> None:
        ds = DualStorage(local_base_path="data")
        assert ds.write_bronze({"x": 1}, "linkedin", "2025-01-01") is True

    def test_local_only_write_silver(self) -> None:
        ds = DualStorage(local_base_path="data")
        assert ds.write_silver({"x": 1}, "jobs", "2025-01-01") is True

    def test_local_only_write_gold(self) -> None:
        ds = DualStorage(local_base_path="data")
        assert ds.write_gold({"x": 1}, "jobs", "2025-01-01") is True

    def test_local_only_read_layers(self) -> None:
        ds = DualStorage(local_base_path="data")
        assert ds.read_bronze("src", "ts") is None
        assert ds.read_silver("ent", "ts") is None
        assert ds.read_gold("ent", "ts") is None

    def test_dual_mode_enabled(self) -> None:
        ds = DualStorage(
            local_base_path="data",
            bigquery_project="my-project",
            enable_bigquery=True,
        )
        assert ds.bigquery_storage is not None
        assert ds.write_bronze({"x": 1}, "src", "2025-01-01") is True


# ---------------------------------------------------------------------------
# DataLineage
# ---------------------------------------------------------------------------


class TestDataLineage:
    def test_record_bronze(self) -> None:
        dl = DataLineage()
        lid = dl.record_bronze_ingestion("linkedin", 100, "2025-01-01")
        assert lid.startswith("bronze_")
        info = dl.get_lineage(lid)
        assert info is not None
        assert info["record_count"] == 100

    def test_record_silver(self) -> None:
        dl = DataLineage()
        b_id = dl.record_bronze_ingestion("indeed", 50, "2025-01-01")
        s_id = dl.record_silver_transformation(b_id, 45, 0.82)
        info = dl.get_lineage(s_id)
        assert info is not None
        assert info["quality_score"] == 0.82
        assert info["parent"] == b_id

    def test_record_gold(self) -> None:
        dl = DataLineage()
        b_id = dl.record_bronze_ingestion("indeed", 50, "2025-01-01")
        g_id = dl.record_gold_enrichment(b_id, 40, "all-MiniLM-L6-v2")
        info = dl.get_lineage(g_id)
        assert info is not None
        assert info["embedding_model"] == "all-MiniLM-L6-v2"

    def test_get_missing_lineage(self) -> None:
        dl = DataLineage()
        assert dl.get_lineage("nonexistent") is None
