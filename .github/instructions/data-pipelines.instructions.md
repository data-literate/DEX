---
applyTo: "src/careerdex/**/*.py,src/weatherdex/**/*.py,src/**/data/**/*.py,src/**/lakehouse/**/*.py,src/**/warehouse/**/*.py"
---

# Data Pipelines — Project Specifics

## Architecture
- Medallion pattern: Bronze (raw) → Silver (cleaned) → Gold (aggregated)
- Pipelines must be idempotent — log processing counts/IDs

## Orchestration
- Airflow DAGs: `src/careerdex/dags/` (use `default_args`, XCom, clear task deps)
- PySpark: `src/weatherdex/ml/` (large-scale transforms)

## Quality & Governance
- `SchemaRegistry`: `packages/dataenginex/src/dataenginex/data/registry.py` (schema versioning)
- `DataCatalog`: `packages/dataenginex/src/dataenginex/lakehouse/catalog.py` (dataset discovery)
- Data contracts: Pydantic schemas in `packages/dataenginex/src/dataenginex/core/schemas.py`
- Validators: `packages/dataenginex/src/dataenginex/core/validators.py`

## Transform & Lineage
- `TransformPipeline`: composable transforms (`packages/dataenginex/src/dataenginex/warehouse/transforms.py`)
- `PersistentLineage`: data lineage tracking (`packages/dataenginex/src/dataenginex/warehouse/lineage.py`)
- Partitioning: `DatePartitioner`, `HashPartitioner` (`packages/dataenginex/src/dataenginex/lakehouse/partitioning.py`)
- Profiling: `packages/dataenginex/src/dataenginex/data/profiler.py`

## Project Map
- `src/careerdex/` — DAGs, models, phases
- `src/weatherdex/` — config, PySpark ML, notebooks
- `packages/dataenginex/src/dataenginex/data/` — connectors, profiler, registry
- `packages/dataenginex/src/dataenginex/lakehouse/` — catalog, partitioning, storage
- `packages/dataenginex/src/dataenginex/warehouse/` — transforms, lineage, metrics

## Testing
- See `tests/unit/test_data.py`, `test_medallion.py`, `test_warehouse.py`
