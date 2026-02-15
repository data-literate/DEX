"""
Core framework - schemas, validators, and medallion architecture.
"""

from .medallion_architecture import (  # noqa: F401
    DataLayer,
    LayerConfiguration,
    MedallionArchitecture,
    StorageFormat,
)
from .pipeline_config import PipelineConfig, PipelineMetrics  # noqa: F401
from .schemas import JobPosting, JobSourceEnum, UserProfile  # noqa: F401
from .validators import (  # noqa: F401
    DataHash,
    DataQualityChecks,
    QualityScorer,
    SchemaValidator,
    ValidationReport,
)

__all__ = [
    "JobPosting",
    "JobSourceEnum",
    "UserProfile",
    "SchemaValidator",
    "DataQualityChecks",
    "DataHash",
    "QualityScorer",
    "ValidationReport",
    "MedallionArchitecture",
    "DataLayer",
    "StorageFormat",
    "LayerConfiguration",
    "PipelineConfig",
    "PipelineMetrics",
]
