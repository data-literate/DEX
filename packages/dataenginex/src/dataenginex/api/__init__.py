"""Reusable API components — auth, health, errors, pagination, rate limiting.

Public API::

    from dataenginex.api import (
        HealthChecker, HealthStatus, ComponentHealth,
        APIHTTPException, BadRequestError, NotFoundError, ServiceUnavailableError,
        PaginatedResponse, paginate,
        AuthMiddleware, AuthUser, create_token, decode_token,
        RateLimiter, RateLimitMiddleware,
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
    # Rate limiting
    "RateLimiter",
    "RateLimitMiddleware",
]
