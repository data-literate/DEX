---
description: "Create a new Airflow DAG for CareerDEX"
tools: ["search/codebase", "execute/runInTerminal", "execute/getTerminalOutput", "read/terminalLastCommand", "read/terminalSelection"]
---

Create a new Airflow DAG for the CareerDEX data pipeline.

## Requirements

1. **Location** — `src/careerdex/dags/`
2. **Structure**:
   - Use `default_args` with owner, retries, retry_delay
   - Define clear task dependencies with `>>` operator
   - Use XCom for inter-task data passing
   - DAG must be idempotent (safe to rerun)
3. **Medallion pattern**:
   - Bronze: raw ingestion → Silver: cleaned/validated → Gold: aggregated
   - Log processing counts and record IDs at each stage
4. **Data quality**:
   - Validate schemas at entry point using project validators
   - Reference `packages/dataenginex/src/dataenginex/core/validators.py` for patterns
5. **Logging**:
   - Use `from loguru import logger` (not structlog in data pipelines)
   - Log with structured key-value pairs: `logger.info("processed records", count=n)`
6. **Error handling**:
   - Catch specific exceptions, log context, re-raise
   - Never silently swallow errors
7. **Tests** — Add tests in `tests/unit/` following patterns in `test_data.py`

Follow existing DAG patterns in `src/careerdex/dags/`.
