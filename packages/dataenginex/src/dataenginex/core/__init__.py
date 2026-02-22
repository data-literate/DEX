"""Core framework — schemas, validators, medallion architecture, pipeline config.

Public API::

    from dataenginex.core import (
        # Medallion
        MedallionArchitecture, DataLayer, StorageFormat, LayerConfiguration,
        # Pipeline
        PipelineConfig, PipelineMetrics,
        # Schemas
        JobPosting, JobSourceEnum, UserProfile,
        ErrorDetail, ErrorResponse, RootResponse, HealthResponse,
        DataQualityReport, PipelineExecutionMetadata,
        # Validators
        SchemaValidator, DataQualityChecks, DataHash,
        QualityScorer, ValidationReport,
    )
"""

from __future__ import annotations

from .medallion_architecture import (
    DataLayer,
    LayerConfiguration,
    MedallionArchitecture,
    StorageFormat,
)
from .pipeline_config import PipelineConfig, PipelineMetrics
from .schemas import (
    DataQualityReport,
    ErrorDetail,
    ErrorResponse,
    HealthResponse,
    JobPosting,
    JobSourceEnum,
    PipelineExecutionMetadata,
    RootResponse,
    UserProfile,
)
from .validators import (
    DataHash,
    DataQualityChecks,
    QualityScorer,
    SchemaValidator,
    ValidationReport,
)

__all__ = [
    # Medallion architecture
    "DataLayer",
    "LayerConfiguration",
    "MedallionArchitecture",
    "StorageFormat",
    # Pipeline
    "PipelineConfig",
    "PipelineMetrics",
    # Schemas
    "DataQualityReport",
    "ErrorDetail",
    "ErrorResponse",
    "HealthResponse",
    "JobPosting",
    "JobSourceEnum",
    "PipelineExecutionMetadata",
    "RootResponse",
    "UserProfile",
    # Validators
    "DataHash",
    "DataQualityChecks",
    "QualityScorer",
    "SchemaValidator",
    "ValidationReport",
]
