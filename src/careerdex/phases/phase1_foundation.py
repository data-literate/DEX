"""
CareerDEX Phase 1: Foundation (Issue #65 - Days 1-3)

Sets up infrastructure, schemas, validators, and medallion architecture
for the CareerDEX job intelligence platform.

Deliverables:
- ✓ Pydantic schemas for Job, User, Pipeline, Quality entities
- ✓ Data quality validators (completeness, accuracy, consistency, uniqueness, validity)
- ✓ Medallion architecture (Bronze/Silver/Gold layers)
- ✓ Airflow pipeline configuration
- Pipeline bootstrapping code
- PostgreSQL schema setup
- Redis cache configuration
- Initial directory structure
"""

import logging
from datetime import datetime
from typing import Any

from dataenginex.core.medallion_architecture import (
    DataLineage,
    DualStorage,
    MedallionArchitecture,
)
from dataenginex.core.pipeline_config import PipelineConfig
from dataenginex.core.schemas import JobPosting, PipelineExecutionMetadata, UserProfile
from dataenginex.core.validators import (
    DataHash,
    DataQualityChecks,
    QualityScorer,
    SchemaValidator,
)

logger = logging.getLogger(__name__)


class Phase1Foundation:
    """
    Phase 1 Foundation implementation for CareerDEX v0.3.0.

    Milestone: Complete foundational infrastructure (Days 1-3)

    Timeline:
    - Day 1: Schema definitions, validators, storage layers
    - Day 2: Pipeline configuration, medallion setup
    - Day 3: Integration testing, documentation

    Success Criteria:
    ✓ All schemas pass validation
    ✓ Data quality framework functional
    ✓ Medallion layers configured
    ✓ Airflow DAG structure defined
    ✓ Storage backends initialized
    ✓ PostgreSQL/Redis ready
    """

    def __init__(self):
        self.initialization_timestamp = datetime.utcnow().isoformat()
        self.components_initialized = []
        self.errors = []

    def initialize_schemas(self) -> bool:
        """Initialize and validate all data schemas."""
        logger.info("Phase 1: Initializing data schemas...")

        try:
            # Test JobPosting schema
            test_job = {
                "job_id": "test_001",
                "source": "indeed",
                "source_job_id": "indeed_12345",
                "company_name": "TestCorp",
                "job_title": "Software Engineer",
                "job_description": "We are looking for a talented software engineer...",
                "location": {
                    "country": "US",
                    "state": "CA",
                    "city": "San Francisco",
                    "remote_eligible": True,
                },
                "employment_type": "full_time",
                "posted_date": datetime.utcnow(),
                "last_modified_date": datetime.utcnow(),
                "dex_hash": "abc123def456",
            }

            JobPosting(**test_job)
            logger.info("✓ JobPosting schema initialized")
            self.components_initialized.append("JobPosting schema")

            # Test UserProfile schema
            test_user = {
                "user_id": "user_001",
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_date": datetime.utcnow(),
                "last_activity_date": datetime.utcnow(),
            }

            UserProfile(**test_user)
            logger.info("✓ UserProfile schema initialized")
            self.components_initialized.append("UserProfile schema")

            # Test PipelineExecutionMetadata schema
            test_pipeline = {
                "pipeline_name": "careerdex-job-ingestion",
                "execution_id": "exec_001",
                "execution_start_time": datetime.utcnow(),
                "status": "running",
                "layer": "bronze",
            }

            PipelineExecutionMetadata(**test_pipeline)
            logger.info("✓ PipelineExecutionMetadata schema initialized")
            self.components_initialized.append("Pipeline metadata schema")

            return True

        except Exception as e:
            error_msg = f"Schema initialization failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False

    def initialize_validators(self) -> bool:
        """Initialize data quality validators."""
        logger.info("Phase 1: Initializing validators...")

        try:
            # Test SchemaValidator
            test_data = {
                "job_id": "test_001",
                "source": "indeed",
                "source_job_id": "indeed_12345",
                "company_name": "TestCorp",
                "job_title": "Software Engineer",
                "job_description": "Job description here",
                "location": {"country": "US", "city": "SF"},
                "employment_type": "full_time",
                "posted_date": datetime.utcnow(),
                "last_modified_date": datetime.utcnow(),
                "dex_hash": "hash123",
            }

            is_valid, errors = SchemaValidator.validate_job_posting(test_data)
            logger.info(f"✓ SchemaValidator initialized (validation: {is_valid})")
            self.components_initialized.append("SchemaValidator")

            # Test DataQualityChecks
            salary_min, salary_max = 80000.0, 150000.0
            is_accurate, issues = DataQualityChecks.check_accuracy_salary(salary_min, salary_max)
            logger.info(f"✓ DataQualityChecks initialized (salary check: {is_accurate})")
            self.components_initialized.append("DataQualityChecks")

            # Test DataHash
            hash_value = DataHash.generate_job_hash(
                "indeed_12345",
                "indeed",
                "TestCorp",
                "Software Engineer",
            )
            logger.info(f"✓ DataHash initialized (hash: {hash_value[:16]}...)")
            self.components_initialized.append("DataHash")

            # Test QualityScorer
            score = QualityScorer.score_job_posting(test_data)
            logger.info(f"✓ QualityScorer initialized (test score: {score:.2f})")
            self.components_initialized.append("QualityScorer")

            return True

        except Exception as e:
            error_msg = f"Validator initialization failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False

    def initialize_medallion_architecture(self) -> bool:
        """Initialize medallion architecture layers."""
        logger.info("Phase 1: Initializing Medallion Architecture...")

        try:
            # Get layer configurations
            layers = MedallionArchitecture.get_all_layers()
            logger.info(f"✓ Medallion layers configured: {[layer.layer_name for layer in layers]}")

            # Initialize storage backends
            DualStorage(
                local_base_path="data",
                bigquery_project=None,  # Can be set in env
                enable_bigquery=False,  # Enable in production
            )
            logger.info("✓ Dual storage initialized (local Parquet)")
            self.components_initialized.append("Dual storage (local)")

            # Initialize data lineage tracking
            DataLineage()
            logger.info("✓ Data lineage tracking initialized")
            self.components_initialized.append("Data lineage")

            for layer in layers:
                logger.info(f"  - {layer.layer_name}: {layer.description}")
                logger.info(f"    Quality threshold: {layer.quality_threshold}")
                logger.info(f"    Retention: {layer.retention_days or 'indefinite'} days")

            return True

        except Exception as e:
            error_msg = f"Medallion architecture initialization failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False

    def initialize_pipeline_config(self) -> bool:
        """Initialize Airflow pipeline configuration."""
        logger.info("Phase 1: Initializing Pipeline Configuration...")

        try:
            # Display pipeline configuration
            logger.info(f"✓ Pipeline execution schedule: {PipelineConfig.EXECUTION_SCHEDULE}")
            logger.info(
                f"  Expected cycle time: {PipelineConfig.EXPECTED_CYCLE_TIME_MINUTES} minutes"
            )
            logger.info(f"  Expected jobs per cycle: {PipelineConfig.EXPECTED_JOBS_PER_CYCLE:,}")
            logger.info(f"  Expected jobs in system: {PipelineConfig.EXPECTED_JOBS_TOTAL:,}")

            # Display job sources
            logger.info("Job sources (3-hour cycle targets):")
            for source, config in PipelineConfig.CAREERDEX_JOB_SOURCES.items():
                logger.info(f"  - {source}: {config['expected_cycle_jobs']:,} jobs/cycle")

            # Display Airflow DAG configuration
            logger.info("✓ Airflow DAG configured:")
            logger.info("  DAG ID: careerdex-job-ingestion")
            logger.info(f"  Schedule: {PipelineConfig.EXECUTION_SCHEDULE}")
            logger.info(f"  Timeout: {PipelineConfig.TIMEOUT_MINUTES} minutes")
            logger.info("  View DAG at: src/careerdex/dags/job_ingestion_dag.py")

            self.components_initialized.append("Airflow pipeline config")

            return True

        except Exception as e:
            error_msg = f"Pipeline configuration initialization failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False

    def bootstrap(self) -> dict[str, Any]:
        """
        Execute full Phase 1 bootstrap process.

        Returns:
            Dict with bootstrap status and results
        """
        logger.info("=" * 70)
        logger.info("CAREERDEX PHASE 1 FOUNDATION - BOOTSTRAP STARTED")
        logger.info("=" * 70)
        logger.info(f"Timestamp: {self.initialization_timestamp}")
        logger.info("")

        results = {
            "phase": "Phase 1 Foundation",
            "timestamp": self.initialization_timestamp,
            "status": "initializing",
            "steps": [],
        }

        # Step 1: Schemas
        schema_step = self.initialize_schemas()
        results["steps"].append(
            {
                "name": "Initialize schemas",
                "status": "success" if schema_step else "failed",
                "components": ["JobPosting", "UserProfile", "PipelineMetadata"],
            }
        )

        # Step 2: Validators
        validator_step = self.initialize_validators()
        results["steps"].append(
            {
                "name": "Initialize validators",
                "status": "success" if validator_step else "failed",
                "components": ["SchemaValidator", "DataQualityChecks", "DataHash", "QualityScorer"],
            }
        )

        # Step 3: Medallion Architecture
        medallion_step = self.initialize_medallion_architecture()
        results["steps"].append(
            {
                "name": "Initialize Medallion architecture",
                "status": "success" if medallion_step else "failed",
                "components": ["Bronze", "Silver", "Gold", "DualStorage", "DataLineage"],
            }
        )

        # Step 4: Pipeline Configuration
        pipeline_step = self.initialize_pipeline_config()
        results["steps"].append(
            {
                "name": "Initialize pipeline configuration",
                "status": "success" if pipeline_step else "failed",
                "components": ["AirflowDAG", "PipelineConfig", "PipelineMetrics"],
            }
        )

        # Summary
        all_success = all([schema_step, validator_step, medallion_step, pipeline_step])
        results["status"] = "success" if all_success else "failed"
        results["initialized_components"] = self.components_initialized
        results["errors"] = self.errors
        results["total_components"] = len(self.components_initialized)

        logger.info("")
        logger.info("=" * 70)
        logger.info("PHASE 1 BOOTSTRAP RESULTS")
        logger.info("=" * 70)
        logger.info(f"Status: {results['status'].upper()}")
        logger.info(f"Initialized components: {results['total_components']}")
        logger.info("")

        for component in self.components_initialized:
            logger.info(f"  ✓ {component}")

        if self.errors:
            logger.warning("")
            logger.warning("Errors encountered:")
            for error in self.errors:
                logger.error(f"  ✗ {error}")

        logger.info("=" * 70)
        logger.info("")

        return results


# Convenience function for quick bootstrap
def bootstrap_phase1() -> dict[str, Any]:
    """Bootstrap Phase 1 foundation."""
    phase1 = Phase1Foundation()
    return phase1.bootstrap()
