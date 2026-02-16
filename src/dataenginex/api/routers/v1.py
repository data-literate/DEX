"""
Versioned API router — ``/api/v1/`` endpoints for DEX.

Groups data-pipeline, warehouse, and system endpoints under a versioned
prefix so that breaking changes can be introduced via ``/api/v2/`` later.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from dataenginex.api.pagination import PaginatedResponse, paginate

router = APIRouter(prefix="/api/v1", tags=["v1"])


# ---------------------------------------------------------------------------
# Data pipeline endpoints
# ---------------------------------------------------------------------------


@router.get("/data/sources", response_model=PaginatedResponse)
def list_data_sources(cursor: str | None = None, limit: int = 20) -> PaginatedResponse:
    """List registered data sources (derived from pipeline config)."""
    from dataenginex.core.pipeline_config import PipelineConfig

    sources: list[dict[str, Any]] = [
        {"name": name, "type": cfg.get("type", "unknown"), "status": "active"}
        for name, cfg in PipelineConfig.CAREERDEX_JOB_SOURCES.items()
    ]
    return paginate(sources, cursor=cursor, limit=limit)


@router.get("/data/quality")
def data_quality_summary() -> dict[str, Any]:
    """Return a summary of data quality metrics.

    .. note::
        Scores are **placeholder values** until the quality-tracking
        subsystem is wired in.  See Issue backlog for live metrics epic.
    """
    # TODO(#future): Replace with live metrics from DataProfiler / quality store
    return {
        "overall_score": 0.0,
        "dimensions": {
            "completeness": 0.0,
            "accuracy": 0.0,
            "consistency": 0.0,
            "timeliness": 0.0,
            "uniqueness": 0.0,
        },
        "layer_scores": {
            "bronze": 0.0,
            "silver": 0.0,
            "gold": 0.0,
        },
        "_note": "Placeholder — connect quality store for live data",
    }


# ---------------------------------------------------------------------------
# Warehouse endpoints
# ---------------------------------------------------------------------------


@router.get("/warehouse/layers")
def list_warehouse_layers() -> dict[str, Any]:
    """Return medallion layer configuration."""
    from dataenginex.core.medallion_architecture import MedallionArchitecture

    layers = MedallionArchitecture.get_all_layers()
    return {
        "layers": [
            {
                "name": lc.layer_name,
                "description": lc.description,
                "purpose": lc.purpose,
                "format": lc.storage_format.value,
                "quality_threshold": lc.quality_threshold,
                "retention_days": lc.retention_days,
            }
            for lc in layers
        ]
    }


@router.get("/warehouse/lineage/{event_id}")
def get_lineage(event_id: str) -> dict[str, Any]:
    """Look up a lineage event by ID (placeholder)."""
    return {
        "event_id": event_id,
        "message": "Lineage tracking available — connect PersistentLineage for live data",
    }


# ---------------------------------------------------------------------------
# System endpoints
# ---------------------------------------------------------------------------


@router.get("/system/config")
def system_config() -> dict[str, Any]:
    """Return non-sensitive system configuration."""
    from dataenginex.core.pipeline_config import PipelineConfig

    return {
        "schedule": PipelineConfig.EXECUTION_SCHEDULE,
        "expected_jobs_per_cycle": PipelineConfig.EXPECTED_JOBS_PER_CYCLE,
        "timeout_minutes": PipelineConfig.TIMEOUT_MINUTES,
        "sources": list(PipelineConfig.CAREERDEX_JOB_SOURCES.keys()),
    }
