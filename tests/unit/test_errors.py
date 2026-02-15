"""Tests for custom API exception types."""

from __future__ import annotations

from dataenginex.api.errors import (
    APIHTTPException,
    BadRequestError,
    NotFoundError,
    ServiceUnavailableError,
)
from dataenginex.core.schemas import ErrorDetail


class TestAPIHTTPException:
    def test_basic(self) -> None:
        exc = APIHTTPException(status_code=418, message="teapot")
        assert exc.status_code == 418
        assert exc.detail == "teapot"
        assert exc.code == "api_error"
        assert exc.details is None

    def test_with_details(self) -> None:
        detail = ErrorDetail(field="x", message="bad", type="val")
        exc = APIHTTPException(
            status_code=400,
            message="oops",
            code="custom",
            details=[detail],
        )
        assert exc.code == "custom"
        assert exc.details == [detail]


class TestBadRequestError:
    def test_defaults(self) -> None:
        exc = BadRequestError()
        assert exc.status_code == 400
        assert exc.code == "bad_request"

    def test_custom_message(self) -> None:
        exc = BadRequestError(message="missing field")
        assert exc.detail == "missing field"


class TestNotFoundError:
    def test_defaults(self) -> None:
        exc = NotFoundError()
        assert exc.status_code == 404
        assert exc.code == "not_found"

    def test_custom_message(self) -> None:
        exc = NotFoundError(message="job not found")
        assert exc.detail == "job not found"


class TestServiceUnavailableError:
    def test_defaults(self) -> None:
        exc = ServiceUnavailableError()
        assert exc.status_code == 503
        assert exc.code == "service_unavailable"

    def test_custom_message(self) -> None:
        exc = ServiceUnavailableError(message="DB down")
        assert exc.detail == "DB down"
