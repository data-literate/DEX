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
poetry run python notebooks/feature_engineering.py
```

Train models:
```bash
poetry run python notebooks/train_model.py
```

Analyze predictions:
```bash
poetry run python notebooks/analyze_predictions.py
```
