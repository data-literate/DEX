# Weather Pipeline - Reference Implementation

**Reference pipeline implementation for multi-layer architecture**

## Overview

The Weather Pipeline is a complete, working implementation of the DEX framework's medallion architecture. It serves as a template for all future projects (like CareerDEX).

**Status**: Complete Reference Implementation  
**Purpose**: Learn DEX patterns, validate architecture, reuse for other projects

## 📚 Documentation

- **[START HERE](../../src/weatherdex/START_HERE.md)** - Quick start guide
- **[Pipeline README](../../src/weatherdex/README.txt)** - Overview and structure  
- **[ML Implementation Guide](../../src/weatherdex/ML_README.md)** - Model training and integration
- **[ML Implementation Summary](../../src/weatherdex/ML_IMPLEMENTATION_SUMMARY.txt)** - Execution summary
- **[Execution Checklist](../../src/weatherdex/EXECUTION_CHECKLIST.md)** - Task tracking

## What You'll Learn

This reference implementation demonstrates:

- **Data Ingestion**: Fetching external data (weather API)
- **Bronze Layer**: Raw data storage and schema validation
- **Silver Layer**: Data cleaning, validation, transformations
- **Gold Layer**: Feature engineering and aggregations
- **ML Integration**: Training models on processed data
- **Airflow Orchestration**: DAG configuration and 3-hour cycles
- **Monitoring**: Data quality checks and metrics
- **Testing**: Unit and integration test patterns

## Quick Start

```bash
# See START_HERE.md for complete setup
cd src/weatherdex

# Run pipeline locally
airflow dags trigger weather_pipeline

# View results
ls ~/data/weather/bronze/
ls ~/data/weather/silver/
ls ~/data/weather/gold/
```

## Key Files

- `core/` - Data fetching and transformation logic
- `ml/` - ML model training and prediction
- `config/` - Configuration and schema definitions
- `notebooks/` - Analysis and exploration notebooks

## How to Adapt for Your Project

1. Copy the structure: `src/{project_name}/`
2. Update configs in `config/schema_definitions.py`
3. Replace fetchers in `core/fetch_*.py`
4. Implement business logic transformations
5. Add ML models in `ml/`
6. Create Airflow DAG similar to weather pipeline

## Reference Links

- **DEX Framework**: [docs/common/ARCHITECTURE.md](../common/ARCHITECTURE.md)
- **Medallion Architecture**: [docs/adr/0001-medallion-architecture.md](../adr/0001-medallion-architecture.md)
- **Development Guide**: [docs/common/DEVELOPMENT.md](../common/DEVELOPMENT.md)

---

**Documentation Hub**: [See docs/README.md](../README.md)
