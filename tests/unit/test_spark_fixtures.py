"""Tests for PySpark fixtures — validates Spark local-mode session and sample DataFrames.

These tests are skipped when PySpark is not installed
(requires ``uv sync --group data``).
"""

from __future__ import annotations

from typing import Any

import pytest

from tests.conftest import requires_pyspark


@requires_pyspark
class TestSparkSession:
    """Verify the session-scoped ``spark`` fixture."""

    def test_session_is_active(self, spark: Any) -> None:
        assert spark is not None
        # SparkContext should report a local master
        assert "local" in spark.sparkContext.master

    def test_create_dataframe(self, spark: Any) -> None:
        df = spark.createDataFrame([(1, "a"), (2, "b")], schema=["id", "val"])
        assert df.count() == 2


@requires_pyspark
class TestJobDataFrame:
    """Verify the ``spark_df_jobs`` fixture."""

    def test_row_count(self, spark_df_jobs: Any) -> None:
        assert spark_df_jobs.count() == 5

    def test_columns(self, spark_df_jobs: Any) -> None:
        expected = {"job_id", "source", "company_name", "job_title", "salary_min", "salary_max"}
        assert set(spark_df_jobs.columns) == expected

    def test_filter(self, spark_df_jobs: Any) -> None:
        linkedin = spark_df_jobs.filter("source = 'linkedin'")
        assert linkedin.count() >= 1


@requires_pyspark
class TestWeatherDataFrame:
    """Verify the ``spark_df_weather`` fixture."""

    def test_row_count(self, spark_df_weather: Any) -> None:
        assert spark_df_weather.count() == 5

    def test_columns(self, spark_df_weather: Any) -> None:
        expected = {"city", "date", "temp_c", "humidity", "wind_speed_kmh"}
        assert set(spark_df_weather.columns) == expected


@requires_pyspark
class TestEmptyDataFrame:
    """Verify the ``spark_df_empty`` fixture."""

    def test_empty(self, spark_df_empty: Any) -> None:
        assert spark_df_empty.count() == 0

    def test_schema(self, spark_df_empty: Any) -> None:
        assert "id" in spark_df_empty.columns


@pytest.mark.skipif(True, reason="Always skip — validates skip machinery works")
class TestSkipMachinery:
    def test_never_runs(self) -> None:
        raise AssertionError("This should never execute")
