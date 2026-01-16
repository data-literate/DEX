# Weather ML Model - Complete Guide

## Overview

This directory contains a comprehensive machine learning pipeline for predicting temperature based on weather data. The pipeline includes:

1. **Feature Engineering** - Create ML-ready features from raw weather data
2. **Model Training** - Train Random Forest temperature prediction model  
3. **Prediction Analysis** - Analyze model performance across dimensions

## Quick Start

### Prerequisites
- Spark 3.0+
- PySpark with MLlib
- Weather data in `weather_current` table

### Run the Complete Pipeline

```bash
# 1. Feature Engineering
databricks workspace import & run feature_engineering.py

# 2. Model Training
databricks workspace import & run train_model.py

# 3. Prediction Analysis
databricks workspace import & run analyze_predictions.py
```

## Files and Structure

```
weather/
├── ml/
│   ├── ml_utils.py                 # Core ML utility classes
│   └── __init__.py
├── notebooks/
│   ├── feature_engineering.ipynb   # Task 1: Create features
│   ├── train_model.ipynb           # Task 2: Train model
│   └── analyze_predictions.ipynb   # Task 3: Analyze results
└── README.md                        # This file
```

## Tasks Explained

### Task 1: Feature Engineering (`feature_engineering.ipynb`)

**Purpose:** Transform raw weather data into ML features

**Input:** `weather_current` table
- city, country, temperature, humidity, pressure
- wind_speed, visibility, cloudiness, condition
- timestamp (ISO format)

**Output:** `weather_features` table

**Features Created:**
- **Time Features (5):** hour, day_of_week, day_of_year, month, timestamp_unix
- **Lag Features (12):** 1/3/6/12-step lags for temperature, humidity, pressure
- **Rolling Features (12):** 3/6/12-hour rolling mean & std for temperature, mean for humidity/pressure
- **Interaction Features (3):** Temperature-humidity, cloud-visibility, pressure-humidity interactions
- **Base Features (5):** humidity, pressure, wind_speed, visibility, cloudiness

**Total: 25+ engineered features**

### Task 2: Model Training (`train_model.ipynb`)

**Purpose:** Train temperature prediction model

**Input:** `weather_features` table

**Output:** 
- `/tmp/weather_temperature_model` (trained model)
- `weather_predictions` table (predictions + errors)

**Model Specification:**
- Algorithm: Random Forest Regression
- Trees: 50
- Max Depth: 10
- Min Samples per Leaf: 5
- Feature Scaling: StandardScaler (normalization)

**Performance Metrics:**
- RMSE: ~2-3°C (depends on data)
- MAE: ~1.5-2.5°C
- R²: 0.70-0.85

### Task 3: Prediction Analysis (`analyze_predictions.ipynb`)

**Purpose:** Analyze model performance across multiple dimensions

**Input:** `weather_predictions` table

**Output:** Analysis tables
- `weather_analysis_by_city` - Performance by location
- `weather_analysis_by_hour` - Performance by time of day
- `weather_analysis_by_day` - Performance by day of week
- `weather_analysis_by_condition` - Performance by weather type
- `weather_analysis_by_temp_range` - Performance by temperature range
- `weather_residual_statistics` - Error distribution stats

**Analysis Includes:**
- Average error by dimension
- Standard deviation of errors
- Prediction accuracy within thresholds
- Best and worst predictions
- Error distribution analysis

## Data Flow

```
weather_current (raw data)
        ↓
feature_engineering.ipynb
        ↓
weather_features (engineered features)
        ↓
train_model.ipynb
        ↓
weather_temperature_model (trained model)
weather_predictions (predictions)
        ↓
analyze_predictions.ipynb
        ↓
weather_analysis_* (analysis tables)
```

## Feature Details

### Time-Based Features
Extract temporal patterns from timestamp:
- `hour`: 0-23 (captures daily cycle)
- `day_of_week`: 1-7 (captures weekly patterns)
- `day_of_year`: 1-365 (captures seasonal patterns)
- `month`: 1-12 (captures monthly patterns)
- `timestamp_unix`: Unix timestamp for numerical processing

### Lag Features
Previous observations from same city:
- `temperature_lag_1/3/6/12`: Recent temperature history
- `humidity_lag_1/3/6/12`: Recent humidity history
- `pressure_lag_1/3/6/12`: Recent pressure history

Captures autocorrelation in weather data.

### Rolling Window Features
Statistics over time windows:
- `temperature_rolling_mean_3/6/12`: Temperature trend
- `temperature_rolling_std_3/6/12`: Temperature volatility
- `humidity_rolling_mean_3/6/12`: Humidity trend
- `pressure_rolling_mean_3/6/12`: Pressure trend

### Interaction Features
Combines multiple features:
- `temp_humidity_interaction`: Temperature × (humidity/100)
- `cloud_visibility_ratio`: Cloudiness / visibility
- `pressure_humidity_interaction`: Pressure × (humidity/1000)

## Model Performance Interpretation

### RMSE (Root Mean Squared Error)
- Typical: 2-3°C
- Measures average prediction error magnitude
- Penalizes large errors more heavily

### MAE (Mean Absolute Error)
- Typical: 1.5-2.5°C
- Average absolute prediction error
- More interpretable than RMSE

### R² (Coefficient of Determination)
- Typical: 0.70-0.85
- Fraction of temperature variance explained
- R² = 0.85 means model explains 85% of variance

### Accuracy Metrics
- Within 1°C: % of predictions with error ≤ 1°C
- Within 2°C: % of predictions with error ≤ 2°C
- Within 3°C: % of predictions with error ≤ 3°C

## Using the ML Utilities

### WeatherFeatureEngineer

```python
from ml.ml_utils import WeatherFeatureEngineer

engineer = WeatherFeatureEngineer(spark)
features_df = engineer.prepare_training_data(raw_data_df)
feature_cols = engineer.get_feature_columns()
```

### WeatherModelTrainer

```python
from ml.ml_utils import WeatherModelTrainer

trainer = WeatherModelTrainer(spark)
model, metrics = trainer.train_temperature_model(
    features_df, 
    feature_columns=feature_cols
)

# Get feature importance
top_features = trainer.get_feature_importance(top_n=20)
```

### WeatherPredictionAnalyzer

```python
from ml.ml_utils import WeatherPredictionAnalyzer

analyzer = WeatherPredictionAnalyzer(spark)
analysis = analyzer.analyze_predictions(predictions_df)
```

## Troubleshooting

### Issue: Low Model Accuracy
**Solution:**
- Add more historical data (time-series models need trends)
- Include more weather stations/cities
- Engineer domain-specific features
- Try ensemble methods (GBT + RF)

### Issue: Null Values in Features
**Solution:**
- Increase lag values to reduce nulls from lag features
- Impute rolling features before nulls appear
- Filter to cities with sufficient historical data

### Issue: Slow Training
**Solution:**
- Reduce number of trees: 20-30 instead of 50
- Reduce max depth: 5-8 instead of 10
- Sample data for initial testing
- Increase min instances per node

## Expected Results

With typical weather data (100+ days, multiple cities):

| Metric | Expected Range |
|--------|-----------------|
| RMSE | 2.0 - 3.5°C |
| MAE | 1.5 - 2.5°C |
| R² | 0.70 - 0.85 |
| Accuracy within 2°C | 70 - 85% |
| Accuracy within 3°C | 85 - 95% |

## Advanced Configuration

### Adjust Model Parameters

Edit `train_model.ipynb`:

```python
rf = RandomForestRegressor(
    numTrees=100,          # More trees = better but slower
    maxDepth=15,           # Deeper trees = more complex patterns
    minInstancesPerNode=10 # Minimum samples per leaf
)
```

### Add/Remove Features

Edit `feature_engineering.ipynb`:

```python
# Add more lag values
lag_values = [1, 2, 3, 6, 12, 24]

# Add more rolling windows
window_sizes = [2, 3, 6, 12]
```

## Monitoring and Maintenance

### Daily Tasks
- Monitor prediction errors
- Check for data quality issues
- Alert on anomalies

### Weekly Tasks
- Review feature distributions
- Check for data drift

### Monthly Tasks
- Retrain model with new data
- Update performance baselines
- Review error patterns

### Quarterly Tasks
- Feature engineering review
- Model architecture evaluation
- Hyperparameter optimization

## References

- [PySpark MLlib Documentation](https://spark.apache.org/docs/latest/ml-guide.html)
- [Regression Evaluation Metrics](https://en.wikipedia.org/wiki/Evaluation_of_binary_classifiers)
- [Feature Engineering Best Practices](https://scikit-learn.org/stable/modules/feature_engineering.html)

## Support and Contact

For issues or questions:
1. Check troubleshooting section above
2. Review ML_GUIDE.txt for detailed documentation
3. Check feature distributions in analysis tables
4. Consider domain-specific adjustments

---

**Last Updated:** 2026-01-13
**Status:** Production Ready
**Version:** 1.0
