# Databricks notebook source

# MAGIC %md
# MAGIC # Weather ML - Model Training
# MAGIC Train machine learning model for temperature prediction

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMMAND ----------

# Initialize Spark
spark = SparkSession.builder.appName("WeatherModelTraining").getOrCreate()

# COMMAND ----------

# Load engineered features
try:
    df = spark.table("weather_features")
    logger.info(f"Loaded {df.count()} feature records")
except Exception as e:
    logger.error(f"Failed to load features: {str(e)}")
    raise

# COMMAND ----------

# Select feature columns (exclude IDs, timestamps, and target)
exclude_cols = {
    "city",
    "country",
    "timestamp",
    "temperature",
    "feels_like",
    "condition",
    "description",
    "wind_speed",
    "visibility",
    "cloudiness",
    "timestamp_unix",
}

feature_cols = [col for col in df.columns if col not in exclude_cols]

logger.info(f"Selected {len(feature_cols)} features for training")
logger.info(f"Features: {', '.join(sorted(feature_cols)[:10])}...")

# COMMAND ----------

# Display feature columns
print("All selected features:")
for i, col_name in enumerate(sorted(feature_cols), 1):
    print(f"{i}. {col_name}")

# COMMAND ----------

# Create feature vector
assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol="features",
    handleInvalid="skip",
)

# Create Random Forest model
rf = RandomForestRegressor(
    featuresCol="features",
    labelCol="temperature",
    numTrees=50,
    maxDepth=10,
    minInstancesPerNode=5,
    seed=42,
    featureSubsetStrategy="sqrt",
    subsamplingRate=0.8,
)

# Create pipeline
pipeline = Pipeline(stages=[assembler, rf])

logger.info("Training Random Forest model...")

# COMMAND ----------

# Split data: 80% train, 20% test
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

logger.info(f"Training samples: {train_df.count()}")
logger.info(f"Test samples: {test_df.count()}")

# COMMAND ----------

# Train model
model = pipeline.fit(train_df)
logger.info("✓ Model training complete")

# COMMAND ----------

# Make predictions
predictions = model.transform(test_df)

# COMMAND ----------

# Evaluate model
logger.info("Evaluating model...")

evaluator_rmse = RegressionEvaluator(
    labelCol="temperature",
    predictionCol="prediction",
    metricName="rmse",
)

evaluator_r2 = RegressionEvaluator(
    labelCol="temperature",
    predictionCol="prediction",
    metricName="r2",
)

evaluator_mae = RegressionEvaluator(
    labelCol="temperature",
    predictionCol="prediction",
    metricName="mae",
)

rmse = evaluator_rmse.evaluate(predictions)
r2 = evaluator_r2.evaluate(predictions)
mae = evaluator_mae.evaluate(predictions)

logger.info(f"\n=== MODEL PERFORMANCE ===")
logger.info(f"RMSE (Root Mean Squared Error): {rmse:.4f}°C")
logger.info(f"MAE (Mean Absolute Error):      {mae:.4f}°C")
logger.info(f"R² (Coefficient of Determination): {r2:.4f}")
logger.info(f"Model explains {r2*100:.2f}% of variance")

# COMMAND ----------

# Display sample predictions
logger.info("\nSample Predictions:")
predictions.select(
    "city",
    "timestamp",
    "temperature",
    "prediction",
    "humidity",
    "pressure",
).limit(20).display()

# COMMAND ----------

# Feature importance
rf_model = model.stages[1]

if hasattr(rf_model, "featureImportances"):
    importances = rf_model.featureImportances.toArray()
    feature_importance = sorted(
        zip(feature_cols, importances),
        key=lambda x: x[1],
        reverse=True,
    )

    logger.info("\n=== TOP 15 IMPORTANT FEATURES ===")
    for rank, (feat, importance) in enumerate(feature_importance[:15], 1):
        logger.info(f"{rank:2d}. {feat:40s} {importance:.4f}")

# COMMAND ----------

# Save model
model_path = "/tmp/weather_temperature_model"
logger.info(f"Saving model to {model_path}...")

model.write().overwrite().save(model_path)
logger.info(f"✓ Model saved to {model_path}")

# COMMAND ----------

# Save predictions for analysis
predictions_table = "weather_predictions"
logger.info(f"Saving predictions to {predictions_table}...")

predictions.select(
    "city",
    "country",
    "timestamp",
    "temperature",
    "prediction",
    "humidity",
    "pressure",
    "condition",
    "hour",
    "day_of_week",
    "month",
).write.mode("overwrite").option("mergeSchema", "true").saveAsTable(predictions_table)

logger.info(f"✓ Predictions saved to {predictions_table}")

# COMMAND ----------

logger.info("✓ Model training complete!")
print(f"\nModel Performance Summary:")
print(f"  RMSE: {rmse:.4f}°C")
print(f"  MAE:  {mae:.4f}°C")
print(f"  R²:   {r2:.4f}")
print(f"\nModel saved to: {model_path}")
