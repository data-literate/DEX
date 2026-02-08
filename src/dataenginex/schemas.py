"""Pydantic schemas for API requests and responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    message: str
    version: str


class HealthResponse(BaseModel):
    status: str


class StartupResponse(BaseModel):
    status: str


class ComponentStatus(BaseModel):
    name: str
    status: str
    message: str | None = None
    duration_ms: float | None = None


class ReadinessResponse(BaseModel):
    status: str
    components: list[ComponentStatus]


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str
    type: str | None = None


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str | None = None
    details: list[ErrorDetail] | None = None


class EchoRequest(BaseModel):
    message: str = Field(min_length=1)
    count: int = Field(default=1, ge=1, le=10)


class EchoResponse(BaseModel):
    message: str
    count: int
    echo: list[str]
