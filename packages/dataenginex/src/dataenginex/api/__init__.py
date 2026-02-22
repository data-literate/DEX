"""Reusable API components — auth, health, errors, pagination, rate limiting, quality.

Public API::

    from dataenginex.api import (
        HealthChecker, HealthStatus, ComponentHealth,
        APIHTTPException, BadRequestError, NotFoundError, ServiceUnavailableError,
        PaginatedResponse, paginate,
        AuthMiddleware, AuthUser, create_token, decode_token,
        RateLimiter, RateLimitMiddleware,
        get_quality_store, set_quality_store,
    )
"""

from __future__ import annotations

from .auth import AuthMiddleware, AuthUser, create_token, decode_token
from .errors import (
    APIHTTPException,
    BadRequestError,
    NotFoundError,
    ServiceUnavailableError,
)
from .health import ComponentHealth, HealthChecker, HealthStatus
from .pagination import PaginatedResponse, PaginationMeta, paginate
from .rate_limit import RateLimiter, RateLimitMiddleware
from .routers.v1 import get_quality_store, set_quality_store

__all__ = [
    # Auth
    "AuthMiddleware",
    "AuthUser",
    "create_token",
    "decode_token",
    # Errors
    "APIHTTPException",
    "BadRequestError",
    "NotFoundError",
    "ServiceUnavailableError",
    # Health
    "ComponentHealth",
    "HealthChecker",
    "HealthStatus",
    # Pagination
    "PaginatedResponse",
    "PaginationMeta",
    "paginate",
    # Quality store
    "get_quality_store",
    "set_quality_store",
    # Rate limiting
    "RateLimiter",
    "RateLimitMiddleware",
]
