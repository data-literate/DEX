================================================================================
WEATHER ML PIPELINE - EXECUTION CHECKLIST
================================================================================

Quick Reference Guide for Running the ML Pipeline

================================================================================
PRE-EXECUTION CHECKLIST
================================================================================

Before starting the pipeline, verify:

□ Data Preparation
  □ weather_current table exists and has data
  □ At least 100 observations per city
  □ At least 3 different cities
  □ Timestamp format is ISO 8601 (yyyy-MM-dd'T'HH:mm:ss)
  □ All required columns present:
    - city, country, temperature, humidity, pressure
    - wind_speed, visibility, cloudiness, condition, timestamp

□ Environment Setup
  □ Databricks workspace is available
  □ Spark session is running (or will be created automatically)
  □ Sufficient cluster resources (2+ GB memory recommended)
  □ Write permissions to /tmp/ directory
  □ Create table permissions enabled

□ File Locations
  □ Notebooks are in: pipelines/weather/notebooks/
  □ ML utilities in: pipelines/weather/ml/ml_utils.py
  □ Documentation available locally

================================================================================
STEP 1: FEATURE ENGINEERING (2-3 MINUTES)
================================================================================

Execute: notebooks/feature_engineering.ipynb

Before Running:
□ Open feature_engineering.ipynb
□ Verify weather_current table loads successfully
□ Check data preview (sample rows visible)

During Execution:
□ Cell 1: Libraries imported ✓
□ Cell 2: Data loaded successfully ✓
□ Cell 3: weather_current table opened ✓
□ Cell 4: Time features created ✓
□ Cell 5: Lag features created ✓
□ Cell 6: Rolling window features created ✓
□ Cell 7: Interaction features created ✓
□ Cell 8: Null values handled ✓
□ Cell 9: Feature summary displayed ✓
□ Cell 10: Data saved to weather_features table ✓

Expected Output:
✓ weather_features table created
✓ 25+ engineered features
✓ ~Original data size or slightly larger
✓ All null values removed
✓ Ready for model training

Troubleshooting:
□ If no data loads: Check weather_current table name and format
□ If null errors: Ensure sufficient historical data per city
□ If table save fails: Check write permissions to tables

Next Step: Move to Model Training

================================================================================
STEP 2: MODEL TRAINING (3-5 MINUTES)
================================================================================

Execute: notebooks/train_model.ipynb

Before Running:
□ Verify weather_features table exists (from Step 1)
□ Ensure no other models are running
□ Clear any old /tmp/weather_temperature_model if exists

During Execution:
□ Cell 1: Libraries imported ✓
□ Cell 2: weather_features table loaded ✓
□ Cell 3: Feature columns defined ✓
□ Cell 4: Data split (80/20) ✓
□ Cell 5: ML pipeline built ✓
□ Cell 6: Model training started (will take 1-2 minutes) ✓
□ Cell 7: Performance metrics calculated ✓
□ Cell 8: Feature importance displayed ✓
□ Cell 9: Sample predictions shown ✓
□ Cell 10: Model saved ✓

Expected Output:
✓ Model trained successfully
✓ RMSE: 2.0-3.0°C (typical)
✓ MAE: 1.5-2.5°C (typical)
✓ R²: 0.70-0.85 (typical)
✓ weather_predictions table created
✓ Model saved to /tmp/weather_temperature_model
✓ Feature importance list displayed

Performance Expectations:
Expected RMSE: 2.0-3.0°C
Expected MAE: 1.5-2.5°C
Expected R²: 0.70-0.85
If results are worse:
  → Add more training data
  → Check feature quality
  → Try different hyperparameters

Feature Importance Review:
Top 5 features should typically be:
1. Recent temperature measurements (lag features)
2. Temperature rolling means
3. Hour of day
4. Day of week
5. Humidity or pressure metrics

Troubleshooting:
□ If training is slow: Reduce data size or cluster size
□ If memory error: Reduce dataset or increase cluster memory
□ If model file won't save: Check write permissions to /tmp/
□ If accuracy is low: Verify data quality and feature engineering

Next Step: Move to Prediction Analysis

================================================================================
STEP 3: PREDICTION ANALYSIS (1-2 MINUTES)
================================================================================

Execute: notebooks/analyze_predictions.ipynb

Before Running:
□ Verify weather_predictions table exists (from Step 2)
□ Ensure previous steps completed successfully
□ Have pen/paper ready to note down key metrics

During Execution:
□ Cell 1: Libraries imported ✓
□ Cell 2: Predictions loaded ✓
□ Cell 3: City-wise performance analysis ✓
□ Cell 4: Hourly performance analysis ✓
□ Cell 5: Day-of-week performance analysis ✓
□ Cell 6: Weather condition analysis ✓
□ Cell 7: Residual analysis ✓
□ Cell 8: Temperature range analysis ✓
□ Cell 9: Summary report generated ✓

Expected Output:
✓ weather_analysis_by_city table
✓ weather_analysis_by_hour table
✓ weather_analysis_by_day table
✓ weather_analysis_by_condition table
✓ weather_analysis_by_temp_range table
✓ weather_residual_statistics table

Key Metrics to Review:
├─ Overall Mean Absolute Error: ___________°C
├─ Best performing city: ___________________
├─ Worst performing city: __________________
├─ Best performing hour: ______(0-23)
├─ Worst performing hour: ____(0-23)
├─ Accuracy within 2°C: _________%
└─ Total predictions analyzed: _____________

Analysis Tables Created:
Table: weather_analysis_by_city
  Use for: City-specific accuracy, ranking locations
Table: weather_analysis_by_hour
  Use for: Time-of-day patterns, hourly trends
Table: weather_analysis_by_day
  Use for: Weekly patterns, day-of-week effects
Table: weather_analysis_by_condition
  Use for: Weather type performance
Table: weather_analysis_by_temp_range
  Use for: Performance at different temperatures
Table: weather_residual_statistics
  Use for: Error distribution analysis

Troubleshooting:
□ If tables are empty: Check weather_predictions table contents
□ If analysis is slow: Tables are normal size for given data
□ If some analyses fail: Some columns may not exist in data

Next Step: Review Results and Plan Next Steps

================================================================================
POST-EXECUTION: REVIEW AND VALIDATION
================================================================================

After completing all 3 steps, verify results:

□ Data Quality Validation
  □ Total predictions >= number of test samples
  □ No NaN values in error metrics
  □ Min/max errors are reasonable
  □ Error distributions are roughly normal

□ Model Quality Validation
  □ RMSE is within expected range (2.0-3.0°C)
  □ MAE is within expected range (1.5-2.5°C)
  □ R² is within expected range (0.70-0.85)
  □ Accuracy >50% within 2°C
  □ Feature importance list is non-empty

□ Analysis Quality Validation
  □ All 6 analysis tables created
  □ City analysis has all cities
  □ Hourly analysis has hours 0-23
  □ Condition analysis has all weather types
  □ Residual statistics show reasonable ranges

□ Documentation Review
  □ Read ML_README.md for understanding
  □ Review ML_GUIDE.txt for technical details
  □ Note key findings and metrics

================================================================================
CRITICAL SUCCESS CRITERIA
================================================================================

Verify these must-haves:

✓ Features
  □ weather_features table exists
  □ Has 25+ feature columns
  □ No null values
  □ Proper data types

✓ Model
  □ Model trains without errors
  □ Metrics display successfully
  □ Model file saved to /tmp/
  □ Feature importance extracted

✓ Predictions
  □ Predictions table created
  □ Same row count as test set
  □ Prediction values in reasonable range
  □ Error calculations present

✓ Analysis
  □ All 6 analysis tables created
  □ Analysis results display
  □ Summary report shows metrics
  □ No major errors or warnings

If any ✓ is not achieved → Troubleshoot before continuing!

================================================================================
SAVING KEY METRICS (FOR FUTURE REFERENCE)
================================================================================

Record these baseline metrics:

Date Run: _____________________
Data Size: _________________ rows
Cities Included: _________________________________

Model Metrics:
├─ RMSE: ________________°C
├─ MAE: _________________°C
├─ R²: __________________
└─ Test Samples: _________

Accuracy Metrics:
├─ Within 1°C: _________%
├─ Within 2°C: _________%
└─ Within 3°C: _________%

Top 5 Features:
1. _____________________________
2. _____________________________
3. _____________________________
4. _____________________________
5. _____________________________

Best Performing City: ______________ (MAE: ______°C)
Worst Performing City: _____________ (MAE: ______°C)

Best Performing Hour: _____ (Hour 0-23)
Worst Performing Hour: _____ (Hour 0-23)

Notes/Observations:
_____________________________________________
_____________________________________________
_____________________________________________

================================================================================
NEXT ACTIONS
================================================================================

Immediate (This Week):
□ Review all analysis tables
□ Verify model performance meets expectations
□ Document baseline metrics (see section above)
□ Plan deployment to production

Short Term (This Month):
□ Monitor daily predictions if using live data
□ Compare actual vs predicted accuracy
□ Identify areas for improvement
□ Consider retraining with more data

Medium Term (1-3 Months):
□ Add new features (precipitation, humidity, etc.)
□ Try ensemble methods
□ Optimize hyperparameters
□ Create real-time inference API

Long Term (3+ Months):
□ Expand to more cities/regions
□ Deep learning models
□ Anomaly detection
□ Production deployment

================================================================================
SUPPORT RESOURCES
================================================================================

If you get stuck:

1. Check Documentation
   File: ML_README.md
   Covers: Quick start, usage, troubleshooting

2. Read Technical Guide
   File: ML_GUIDE.txt
   Covers: Architecture, features, advanced topics

3. Review This Checklist
   File: EXECUTION_CHECKLIST.md
   Covers: Step-by-step guidance

4. Check Code Comments
   File: ml/ml_utils.py
   Covers: Function documentation, examples

5. Review Notebook Comments
   Files: notebooks/*.ipynb
   Covers: Inline explanations for each step

Common Issues:
┌─────────────────────────────────────────────────────┐
│ Issue: "Table not found" error                      │
│ Solution: Verify table name, run feature engineering│
├─────────────────────────────────────────────────────┤
│ Issue: Low accuracy                                 │
│ Solution: Add more data, engineer more features     │
├─────────────────────────────────────────────────────┤
│ Issue: Memory error                                 │
│ Solution: Reduce data size or increase cluster      │
├─────────────────────────────────────────────────────┤
│ Issue: Very slow execution                          │
│ Solution: Reduce tree count, use smaller cluster    │
└─────────────────────────────────────────────────────┘

================================================================================
EXECUTION SUMMARY
================================================================================

□ Pre-Execution Checklist Complete: _______
□ Feature Engineering Complete: _______
□ Model Training Complete: _______
□ Prediction Analysis Complete: _______
□ Results Validation Complete: _______
□ Metrics Recorded: _______
□ Next Steps Planned: _______

OVERALL STATUS: _________ (READY / NEEDS ATTENTION / COMPLETED)

Date Completed: ________________
Completed By: __________________
Approval: ______________________

================================================================================
Version: 1.0
Last Updated: 2026-01-13
================================================================================
