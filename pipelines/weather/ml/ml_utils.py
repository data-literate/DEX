"""
Weather ML Utilities Module
============================

Provides reusable ML components for weather prediction models:
- Feature engineering
- Model training
- Evaluation and analysis
- Prediction management

Classes:
    WeatherFeatureEngineer: Creates ML features from raw weather data
    WeatherModelTrainer: Trains temperature prediction models
    WeatherPredictionAnalyzer: Analyzes model predictions
"""

import logging
from typing import Tuple, Dict, Any, List
from datetime import datetime, timedelta

import numpy as np
from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql.functions import (
    col,
    lag,
    lead,
    avg,
    stddev,
    max as spark_max,
    min as spark_min,
    when,
    hour,
    dayofweek,
    dayofyear,
    month,
    unix_timestamp,
    abs as spark_abs,
    round as spark_round,
)
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
    VectorAssembler,
    StandardScaler,
    StringIndexer,
)
from pyspark.ml.regression import RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

logger = logging.getLogger(__name__)


class WeatherFeatureEngineer:
    """Feature engineering for weather ML models."""

    def __init__(self, spark: SparkSession):
        """Initialize feature engineer with Spark session."""
        self.spark = spark

    def create_time_features(self, df: DataFrame) -> DataFrame:
        """Extract time-based features from timestamp."""
        from pyspark.sql.functions import from_unixtime, unix_timestamp

        df = df.withColumn(
            "timestamp_unix",
            unix_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss"),
        )

        df = df.withColumn(
            "hour", hour(from_unixtime(col("timestamp_unix")))
        )
        df = df.withColumn(
            "day_of_week", dayofweek(from_unixtime(col("timestamp_unix")))
        )
        df = df.withColumn(
            "day_of_year", dayofyear(from_unixtime(col("timestamp_unix")))
        )
        df = df.withColumn(
            "month", month(from_unixtime(col("timestamp_unix")))
        )

        return df

    def create_lag_features(
        self, df: DataFrame, target: str = "temperature", lags: List[int] = None
    ) -> DataFrame:
        """Create lag features for temporal patterns."""
        if lags is None:
            lags = [1, 3, 6, 12, 24]

        # Window specification: partitioned by city, ordered by timestamp
        window_spec = Window.partitionBy("city").orderBy("timestamp_unix")

        for lag_val in lags:
            df = df.withColumn(
                f"{target}_lag_{lag_val}",
                lag(col(target), lag_val).over(window_spec),
            )

        return df

    def create_rolling_features(
        self,
        df: DataFrame,
        metrics: List[str] = None,
        window_sizes: List[int] = None,
    ) -> DataFrame:
        """Create rolling window statistics."""
        if metrics is None:
            metrics = ["temperature", "humidity", "pressure"]
        if window_sizes is None:
            window_sizes = [3, 6, 12]

        # Window specification for rolling calculations
        for window_size in window_sizes:
            window_spec = Window.partitionBy("city").orderBy(
                "timestamp_unix"
            ).rangeBetween(
                -(window_size - 1), 0
            )

            for metric in metrics:
                df = df.withColumn(
                    f"{metric}_rolling_mean_{window_size}",
                    avg(col(metric)).over(window_spec),
                )
                df = df.withColumn(
                    f"{metric}_rolling_std_{window_size}",
                    stddev(col(metric)).over(window_spec),
                )

        return df

    def create_interaction_features(self, df: DataFrame) -> DataFrame:
        """Create interaction features."""
        # Temperature and humidity interaction
        df = df.withColumn(
            "temp_humidity_interaction",
            col("temperature") * col("humidity") / 100.0,
        )

        # Cloudiness and visibility interaction
        df = df.withColumn(
            "cloud_visibility_ratio",
            col("cloudiness") / (col("visibility") + 0.1),
        )

        # Pressure and humidity
        df = df.withColumn(
            "pressure_humidity_interaction",
            col("pressure") * col("humidity") / 1000.0,
        )

        return df

    def normalize_features(
        self, df: DataFrame, feature_cols: List[str]
    ) -> Tuple[DataFrame, StandardScaler]:
        """Normalize numerical features."""
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        df = assembler.transform(df)

        scaler = StandardScaler(
            inputCol="features",
            outputCol="features_scaled",
            withMean=True,
            withStd=True,
        )
        scaler_model = scaler.fit(df)
        df = scaler_model.transform(df)

        return df, scaler_model

    def prepare_training_data(
        self, df: DataFrame, target: str = "temperature"
    ) -> DataFrame:
        """Prepare complete training dataset with all features."""
        logger.info("Creating time features...")
        df = self.create_time_features(df)

        logger.info("Creating lag features...")
        df = self.create_lag_features(df, target=target)

        logger.info("Creating rolling window features...")
        df = self.create_rolling_features(df)

        logger.info("Creating interaction features...")
        df = self.create_interaction_features(df)

        # Drop rows with null values from lag features
        df = df.dropna()

        return df


class WeatherModelTrainer:
    """Train ML models for weather prediction."""

    def __init__(self, spark: SparkSession):
        """Initialize trainer with Spark session."""
        self.spark = spark

    def train_temperature_model(
        self,
        df: DataFrame,
        model_type: str = "random_forest",
        test_ratio: float = 0.2,
    ) -> Tuple[PipelineModel, Dict[str, float]]:
        """Train temperature prediction model."""
        # Feature columns (exclude IDs, timestamps, and target)
        feature_cols = [
            col for col in df.columns
            if col
            not in [
                "city",
                "country",
                "timestamp",
                "temperature",
                "feels_like",
                "condition",
                "description",
                "timestamp_unix",
            ]
        ]

        # Create assembler
        assembler = VectorAssembler(
            inputCols=feature_cols, outputCol="features"
        )

        # Create regressor
        if model_type == "random_forest":
            regressor = RandomForestRegressor(
                featuresCol="features",
                labelCol="temperature",
                numTrees=50,
                maxDepth=10,
                seed=42,
            )
        elif model_type == "gbt":
            regressor = GBTRegressor(
                featuresCol="features",
                labelCol="temperature",
                maxDepth=5,
                maxIter=20,
                seed=42,
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        # Create pipeline
        pipeline = Pipeline(stages=[assembler, regressor])

        # Split data
        train_df, test_df = df.randomSplit([1 - test_ratio, test_ratio], seed=42)

        # Train model
        logger.info("Training temperature model...")
        model = pipeline.fit(train_df)

        # Evaluate
        predictions = model.transform(test_df)
        evaluator = RegressionEvaluator(
            labelCol="temperature", predictionCol="prediction"
        )

        rmse = evaluator.evaluate(predictions, {evaluator.metricName: "rmse"})
        r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
        mae = evaluator.evaluate(predictions, {evaluator.metricName: "mae"})

        metrics = {
            "rmse": rmse,
            "r2": r2,
            "mae": mae,
            "test_samples": test_df.count(),
            "train_samples": train_df.count(),
        }

        logger.info(f"Model Performance: RMSE={rmse:.3f}, R²={r2:.3f}, MAE={mae:.3f}")

        return model, metrics

    def get_feature_importance(
        self, model: PipelineModel, feature_cols: List[str]
    ) -> Dict[str, float]:
        """Extract feature importance from trained model."""
        # Get the regressor from pipeline
        regressor = model.stages[-1]

        if hasattr(regressor, "featureImportances"):
            importances = regressor.featureImportances.toArray()
            feature_importance = dict(zip(feature_cols, importances))

            # Sort by importance
            sorted_importance = dict(
                sorted(
                    feature_importance.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            )

            return sorted_importance

        return {}


class WeatherPredictor:
    """Make weather predictions using trained models."""

    def __init__(self, model: PipelineModel, feature_engineer: WeatherFeatureEngineer):
        """Initialize predictor with trained model."""
        self.model = model
        self.feature_engineer = feature_engineer

    def predict(self, df: DataFrame) -> DataFrame:
        """Make temperature predictions."""
        # Engineer features
        df = self.feature_engineer.prepare_training_data(df)

        # Make predictions
        predictions = self.model.transform(df)

        return predictions

    def get_city_forecast(
        self, df: DataFrame, city: str
    ) -> Dict[str, Any]:
        """Get forecast for specific city."""
        city_df = df.filter(col("city") == city)
        predictions = self.predict(city_df)

        forecast_data = predictions.select(
            "city",
            "timestamp",
            "temperature",
            "prediction",
            "humidity",
            "pressure",
            "condition",
        ).collect()

        return {
            "city": city,
            "forecasts": [
                {
                    "timestamp": str(row.timestamp),
                    "actual": row.temperature,
                    "predicted": row.prediction,
                    "humidity": row.humidity,
                    "pressure": row.pressure,
                    "condition": row.condition,
                }
                for row in forecast_data
            ],
        }
