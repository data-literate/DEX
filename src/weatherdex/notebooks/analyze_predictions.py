# Databricks notebook source

# MAGIC %md
# MAGIC # Weather ML - Predictions & Analysis
# MAGIC Make predictions and analyze model performance by city

# COMMAND ----------

import logging

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import abs, col, round

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMMAND ----------

# Initialize Spark
spark = SparkSession.builder.appName("WeatherPredictions").getOrCreate()

# COMMAND ----------

# Load trained model
model_path = "/tmp/weather_temperature_model"
logger.info(f"Loading model from {model_path}...")

try:
    model = PipelineModel.load(model_path)
    logger.info("✓ Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

# COMMAND ----------

# Load prediction data
try:
    predictions = spark.table("weather_predictions")
    logger.info(f"Loaded {predictions.count()} predictions")
except Exception as e:
    logger.error(f"Failed to load predictions: {str(e)}")
    raise

# COMMAND ----------

# Calculate prediction error
predictions = predictions.withColumn("error", col("temperature") - col("prediction"))

predictions = predictions.withColumn("abs_error", abs(col("error")))

predictions = predictions.withColumn(
    "error_pct", round((abs(col("error")) / col("temperature") * 100), 2)
)

# COMMAND ----------

# Performance by city
logger.info("\n=== PERFORMANCE BY CITY ===")

city_performance = (
    predictions.groupBy("city")
    .agg(
        {
            "abs_error": ["avg", "min", "max"],
            "temperature": ["count"],
        }
    )
    .orderBy("avg(abs_error)")
)

city_performance.display()

# COMMAND ----------

# Performance by hour of day
logger.info("\n=== PERFORMANCE BY HOUR ===")

hour_performance = (
    predictions.groupBy("hour")
    .agg(
        {
            "abs_error": ["avg", "min", "max"],
            "prediction": ["count"],
        }
    )
    .orderBy("hour")
)

hour_performance.display()

# COMMAND ----------

# Performance by day of week
logger.info("\n=== PERFORMANCE BY DAY OF WEEK ===")

day_names = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

day_performance = (
    predictions.groupBy("day_of_week")
    .agg(
        {
            "abs_error": ["avg", "min", "max"],
            "prediction": ["count"],
        }
    )
    .orderBy("day_of_week")
)

day_performance.display()

# COMMAND ----------

# Predictions by temperature range
logger.info("\n=== PERFORMANCE BY TEMPERATURE RANGE ===")

predictions_with_range = predictions.withColumn(
    "temp_range", (col("temperature").cast("int") / 5 * 5).cast("string")
)

range_performance = (
    predictions_with_range.groupBy("temp_range")
    .agg(
        {
            "abs_error": ["avg"],
            "prediction": ["count"],
        }
    )
    .orderBy("temp_range")
)

range_performance.display()

# COMMAND ----------

# Best and worst predictions
logger.info("\n=== BEST PREDICTIONS ===")
predictions.orderBy("abs_error").select(
    "city",
    "timestamp",
    "temperature",
    "prediction",
    "abs_error",
    "condition",
).limit(10).display()

# COMMAND ----------

logger.info("\n=== WORST PREDICTIONS ===")
predictions.orderBy(col("abs_error").desc()).select(
    "city",
    "timestamp",
    "temperature",
    "prediction",
    "abs_error",
    "condition",
).limit(10).display()

# COMMAND ----------

# Forecast accuracy by condition
logger.info("\n=== PERFORMANCE BY WEATHER CONDITION ===")

condition_performance = (
    predictions.groupBy("condition")
    .agg(
        {
            "abs_error": ["avg", "min", "max"],
            "prediction": ["count"],
        }
    )
    .orderBy("avg(abs_error)")
)

condition_performance.display()

# COMMAND ----------

# Residual analysis
logger.info("\n=== RESIDUAL ANALYSIS ===")

residuals = predictions.select(
    "error",
    "abs_error",
    "city",
    "hour",
    "day_of_week",
    "condition",
)

residuals.select("abs_error").describe().display()

# COMMAND ----------

# Save analysis results
analysis_table = "weather_analysis"
logger.info(f"Saving analysis to {analysis_table}...")

predictions.select(
    "city",
    "country",
    "timestamp",
    "hour",
    "day_of_week",
    "month",
    "temperature",
    "prediction",
    "error",
    "abs_error",
    "error_pct",
    "humidity",
    "pressure",
    "condition",
).write.mode("overwrite").option("mergeSchema", "true").saveAsTable(analysis_table)

logger.info(f"✓ Analysis saved to {analysis_table}")

# COMMAND ----------

# Summary statistics
avg_abs_error = predictions.agg({"abs_error": "avg"}).collect()[0][0]
max_abs_error = predictions.agg({"abs_error": "max"}).collect()[0][0]
min_abs_error = predictions.agg({"abs_error": "min"}).collect()[0][0]

logger.info("\n=== SUMMARY ===")
logger.info(f"Average Absolute Error: {avg_abs_error:.4f}°C")
logger.info(f"Max Absolute Error:     {max_abs_error:.4f}°C")
logger.info(f"Min Absolute Error:     {min_abs_error:.4f}°C")
logger.info(f"Total Predictions:      {predictions.count()}")

print("\n✓ Prediction analysis complete")
