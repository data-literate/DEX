# Weather ML Models

Machine learning models for weather prediction and analysis.

## Structure

- `ml_utils.py` - ML utilities and helper functions
- `notebooks/` - Jupyter notebooks for model training and analysis
- `models/` - Trained model artifacts and checkpoints

## Models

- **Temperature Prediction** - RandomForest model for temperature forecasting
- **Weather Classification** - Classification models for weather conditions

## Training

Run feature engineering:
```bash
uv run poe weather-feature
```

Train models:
```bash
uv run poe weather-train
```

Analyze predictions:
```bash
uv run poe weather-analyze
```
