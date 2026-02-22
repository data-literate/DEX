"""ML training, model registry, drift detection, and serving.

Public API::

    from dataenginex.ml import (
        BaseTrainer, SklearnTrainer, TrainingResult,
        ModelRegistry, ModelArtifact, ModelStage,
        DriftDetector, DriftReport,
        ModelServer, PredictionRequest, PredictionResponse,
    )
"""

from __future__ import annotations

from .drift import DriftDetector, DriftReport
from .registry import ModelArtifact, ModelRegistry, ModelStage
from .serving import ModelServer, PredictionRequest, PredictionResponse
from .training import BaseTrainer, SklearnTrainer, TrainingResult

__all__ = [
    # Training
    "BaseTrainer",
    "SklearnTrainer",
    "TrainingResult",
    # Registry
    "ModelArtifact",
    "ModelRegistry",
    "ModelStage",
    # Drift
    "DriftDetector",
    "DriftReport",
    # Serving
    "ModelServer",
    "PredictionRequest",
    "PredictionResponse",
]
