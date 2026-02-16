"""
dex-ml — ML training, model registry, drift detection, and serving (Epic #42).

Provides:
    - ``BaseTrainer`` / ``SklearnTrainer`` — pluggable training framework
    - ``ModelRegistry`` — local model versioning and promotion
    - ``DriftDetector`` — statistical drift detection (PSI, basic distribution checks)
    - ``ModelServer`` — lightweight prediction interface
"""

from .drift import DriftDetector, DriftReport
from .registry import ModelArtifact, ModelRegistry, ModelStage
from .serving import ModelServer, PredictionRequest, PredictionResponse
from .training import BaseTrainer, SklearnTrainer, TrainingResult

__all__ = [
    "BaseTrainer",
    "DriftDetector",
    "DriftReport",
    "ModelArtifact",
    "ModelRegistry",
    "ModelServer",
    "ModelStage",
    "PredictionRequest",
    "PredictionResponse",
    "SklearnTrainer",
    "TrainingResult",
]
