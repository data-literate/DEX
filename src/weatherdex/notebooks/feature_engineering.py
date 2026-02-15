# Databricks notebook source

# MAGIC %md
# MAGIC # Weather ML - Feature Engineering
# MAGIC Create features for weather prediction model

# COMMAND ----------

import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    dayofweek,
    dayofyear,
    from_unixtime,
    hour,
    lag,
    month,
    stddev,
    unix_timestamp,
)
from pyspark.sql.window import Window

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMMAND ----------

# Initialize Spark
spark = SparkSession.builder.appName("WeatherFeatures").getOrCreate()

# COMMAND ----------

# Load weather data
try:
    df = spark.table("weather_current")
    logger.info(f"Loaded {df.count()} weather records")
except Exception as e:
    logger.error(f"Failed to load weather data: {str(e)}")
    raise

# COMMAND ----------

# Create time-based features
logger.info("Creating time features...")

df = df.withColumn(
    "timestamp_unix",
    unix_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss"),
)

df = df.withColumn("hour", hour(from_unixtime(col("timestamp_unix"))))
df = df.withColumn("day_of_week", dayofweek(from_unixtime(col("timestamp_unix"))))
df = df.withColumn("day_of_year", dayofyear(from_unixtime(col("timestamp_unix"))))
df = df.withColumn("month", month(from_unixtime(col("timestamp_unix"))))

logger.info("Time features created")

# COMMAND ----------

# Create lag features (previous observations)
logger.info("Creating lag features...")

window_spec = Window.partitionBy("city").orderBy("timestamp_unix")

for lag_val in [1, 3, 6, 12]:
    df = df.withColumn(
        f"temperature_lag_{lag_val}",
        lag(col("temperature"), lag_val).over(window_spec),
    )
    df = df.withColumn(
        f"humidity_lag_{lag_val}",
        lag(col("humidity"), lag_val).over(window_spec),
    )
    df = df.withColumn(
        f"pressure_lag_{lag_val}",
        lag(col("pressure"), lag_val).over(window_spec),
    )

logger.info("Lag features created")

# COMMAND ----------

# Create rolling window statistics
logger.info("Creating rolling window features...")

for window_size in [3, 6, 12]:
    window_spec = (
        Window.partitionBy("city")
        .orderBy("timestamp_unix")
        .rangeBetween(-(window_size - 1), 0)
    )

    # Temperature rolling stats
    df = df.withColumn(
        f"temperature_rolling_mean_{window_size}",
        avg(col("temperature")).over(window_spec),
    )
    df = df.withColumn(
        f"temperature_rolling_std_{window_size}",
        stddev(col("temperature")).over(window_spec),
    )

    # Humidity rolling stats
    df = df.withColumn(
        f"humidity_rolling_mean_{window_size}",
        avg(col("humidity")).over(window_spec),
    )

    # Pressure rolling stats
    df = df.withColumn(
        f"pressure_rolling_mean_{window_size}",
        avg(col("pressure")).over(window_spec),
    )

logger.info("Rolling window features created")

# COMMAND ----------

# Create interaction features
logger.info("Creating interaction features...")

df = df.withColumn(
    "temp_humidity_interaction",
    col("temperature") * col("humidity") / 100.0,
)

df = df.withColumn(
    "cloud_visibility_ratio",
    col("cloudiness") / (col("visibility") + 0.1),
)

df = df.withColumn(
    "pressure_humidity_interaction",
    col("pressure") * col("humidity") / 1000.0,
)

logger.info("Interaction features created")

# COMMAND ----------

# Drop rows with null values from lag features
logger.info(f"Rows before dropping nulls: {df.count()}")
df = df.dropna()
logger.info(f"Rows after dropping nulls: {df.count()}")

# COMMAND ----------

# Save featured data
feature_table = "weather_features"
logger.info(f"Saving features to {feature_table}...")

df.write.mode("overwrite").option("mergeSchema", "true").saveAsTable(feature_table)

logger.info(f"✓ {df.count()} feature records saved to {feature_table}")

# COMMAND ----------

# Show feature statistics
logger.info("Feature Summary:")
df.select(
    "temperature", "humidity", "pressure", "wind_speed", "cloudiness"
).describe().display()

# COMMAND ----------

logger.info("✓ Feature engineering complete")
display(df.select("city", "timestamp", "temperature", "humidity", "pressure").limit(10))  # noqa: F821
