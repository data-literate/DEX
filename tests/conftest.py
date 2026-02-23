"""
Test configuration and fixtures for DEX test suite.

Shared fixtures live here; test files create their own local fixtures
and ``TestClient`` instances as needed.

PySpark fixtures require the ``data`` dependency group
(``uv sync --group data``).  Tests that depend on Spark are
automatically skipped when PySpark is not installed.
"""

from __future__ import annotations

from typing import Any

import pytest

# ---------------------------------------------------------------------------
# PySpark availability guard
# ---------------------------------------------------------------------------

try:
    from pyspark.sql import SparkSession  # type: ignore[import-untyped]

    _HAS_PYSPARK = True
except ImportError:
    _HAS_PYSPARK = False

requires_pyspark = pytest.mark.skipif(
    not _HAS_PYSPARK,
    reason="PySpark not installed (install via `uv sync --group data`)",
)


# ---------------------------------------------------------------------------
# PySpark session fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def spark() -> Any:
    """Session-scoped local-mode SparkSession.

    Reused across all tests in a single pytest run to avoid the overhead
    of starting / stopping the JVM repeatedly.

    Automatically skipped when PySpark is not available.
    """
    if not _HAS_PYSPARK:
        pytest.skip("PySpark not installed")

    session: Any = (
        SparkSession.builder.master("local[1]")
        .appName("DEX-test")
        .config("spark.ui.enabled", "false")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "1")
        .config("spark.sql.warehouse.dir", "/tmp/dex-test-warehouse")
        .config("spark.driver.extraJavaOptions", "-Dderby.system.home=/tmp/dex-derby")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture()
def spark_df_jobs(spark: Any) -> Any:
    """Small Spark DataFrame with sample job-posting rows.

    Columns: job_id, source, company_name, job_title, salary_min, salary_max
    """
    if not _HAS_PYSPARK:
        pytest.skip("PySpark not installed")

    data = [
        ("j1", "linkedin", "Acme Corp", "Software Engineer", 80000, 140000),
        ("j2", "indeed", "Beta Inc", "Data Scientist", 90000, 160000),
        ("j3", "linkedin", "Gamma LLC", "ML Engineer", 100000, 180000),
        ("j4", "glassdoor", "Delta Co", "DevOps Engineer", 85000, 150000),
        ("j5", "indeed", "Acme Corp", "Backend Developer", 75000, 130000),
    ]
    columns = ["job_id", "source", "company_name", "job_title", "salary_min", "salary_max"]
    return spark.createDataFrame(data, schema=columns)


@pytest.fixture()
def spark_df_weather(spark: Any) -> Any:
    """Small Spark DataFrame with sample weather rows.

    Columns: city, date, temp_c, humidity, wind_speed_kmh
    """
    if not _HAS_PYSPARK:
        pytest.skip("PySpark not installed")

    data = [
        ("Seattle", "2025-01-01", 5.0, 82.0, 15.5),
        ("Seattle", "2025-01-02", 4.5, 80.0, 12.0),
        ("New York", "2025-01-01", -2.0, 60.0, 25.0),
        ("New York", "2025-01-02", -1.5, 65.0, 20.0),
        ("Austin", "2025-01-01", 12.0, 45.0, 10.0),
    ]
    columns = ["city", "date", "temp_c", "humidity", "wind_speed_kmh"]
    return spark.createDataFrame(data, schema=columns)


@pytest.fixture()
def spark_df_empty(spark: Any) -> Any:
    """Empty Spark DataFrame with a string-typed ``id`` column."""
    if not _HAS_PYSPARK:
        pytest.skip("PySpark not installed")

    from pyspark.sql.types import (  # type: ignore[import-untyped]
        StringType,
        StructField,
        StructType,
    )

    schema = StructType([StructField("id", StringType(), nullable=True)])
    return spark.createDataFrame([], schema=schema)
