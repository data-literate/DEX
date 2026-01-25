"""
Weather ML Pipeline Notebooks

This module contains Jupyter notebooks for the weather ML pipeline:

1. feature_engineering.ipynb
   - Create ML features from raw weather data
   - Output: weather_features table
   - Duration: 2-3 minutes

2. train_model.ipynb
   - Train Random Forest temperature prediction model
   - Output: Trained model + weather_predictions table
   - Duration: 3-5 minutes

3. analyze_predictions.ipynb
   - Analyze model predictions and performance
   - Output: Multiple analysis tables
   - Duration: 1-2 minutes

Quick Start:
    Execute notebooks in order:
    1. feature_engineering.ipynb (creates features)
    2. train_model.ipynb (trains model)
    3. analyze_predictions.ipynb (analyzes results)

    Total time: 6-10 minutes

Documentation:
    - ML_README.md - Quick start guide
    - ML_GUIDE.txt - Complete reference
    - ML_IMPLEMENTATION_SUMMARY.txt - Implementation overview
"""

__version__ = "1.0"
__author__ = "Weather ML Pipeline"

__all__ = ["feature_engineering", "train_model", "analyze_predictions"]
