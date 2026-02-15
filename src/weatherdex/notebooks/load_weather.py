# Databricks notebook source

# MAGIC %md
# MAGIC # Weather Data - Load
# MAGIC Load extracted weather data to Delta Lake

# COMMAND ----------

import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMMAND ----------

# Configuration
TARGET_TABLE = "weather_current"
MODE = "overwrite"

# COMMAND ----------

# Read extracted data from temporary Delta table
spark = SparkSession.builder.appName("WeatherLoad").getOrCreate()

try:
    df = spark.table("weather_raw_temp")
    record_count = df.count()
    logger.info(f"Loaded {record_count} records from weather_raw_temp")
except Exception as e:
    logger.error(f"Failed to read extracted data: {str(e)}")
    raise

# COMMAND ----------

# Cast columns to proper types

df_typed = df.select(
    col("city").cast("string"),
    col("country").cast("string"),
    col("temperature").cast("double"),
    col("feels_like").cast("double"),
    col("humidity").cast("integer"),
    col("pressure").cast("integer"),
    col("condition").cast("string"),
    col("description").cast("string"),
    col("wind_speed").cast("double"),
    col("visibility").cast("double"),
    col("cloudiness").cast("integer"),
    col("timestamp").cast("string"),
)

# COMMAND ----------

# Write to Delta Lake
try:
    row_count = df_typed.count()
    df_typed.write.mode(MODE).option("mergeSchema", "true").saveAsTable(TARGET_TABLE)

    logger.info(f"✓ Loaded {row_count} records to {TARGET_TABLE}")
except Exception as e:
    logger.error(f"Failed to load data: {str(e)}")
    raise

# COMMAND ----------

# Display results for verification
spark.sql(f"SELECT * FROM {TARGET_TABLE}").display()
