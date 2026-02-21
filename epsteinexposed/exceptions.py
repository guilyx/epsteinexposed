# Credits: Erwin Lejeune — 2026-02-22
"""Custom exceptions for the epsteinexposed package."""

from __future__ import annotations

from typing import Any


class EpsteinExposedAPIError(Exception):
    """Base exception for all Epstein Exposed API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"


class EpsteinExposedValidationError(EpsteinExposedAPIError):
    """Raised for 400 Bad Request (invalid parameters)."""

    def __init__(
        self,
        message: str = "Invalid or missing query parameters",
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=400, response=response)


class EpsteinExposedNotFoundError(EpsteinExposedAPIError):
    """Raised when a resource is not found (404)."""

    def __init__(
        self,
        message: str = "The requested resource does not exist",
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=404, response=response)


class EpsteinExposedRateLimitError(EpsteinExposedAPIError):
    """Raised when the rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded — back off and retry",
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=429, response=response)


class EpsteinExposedServerError(EpsteinExposedAPIError):
    """Raised on server-side failures (5xx)."""

    def __init__(
        self,
        message: str = "Internal server error",
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=500, response=response)
