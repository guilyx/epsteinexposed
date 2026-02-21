# Credits: Erwin Lejeune — 2026-02-22
"""Unofficial Python client for the Epstein Exposed public API."""

from epsteinexposed.async_client import AsyncEpsteinExposed
from epsteinexposed.client import EpsteinExposed
from epsteinexposed.exceptions import (
    EpsteinExposedAPIError,
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
    EpsteinExposedServerError,
    EpsteinExposedValidationError,
)
from epsteinexposed.models import (
    Document,
    Flight,
    PaginatedResponse,
    PaginationMeta,
    Person,
    PersonDetail,
    PersonStats,
    SearchResults,
)

__version__ = "0.1.0"

__all__ = [
    "AsyncEpsteinExposed",
    "Document",
    "EpsteinExposed",
    "EpsteinExposedAPIError",
    "EpsteinExposedNotFoundError",
    "EpsteinExposedRateLimitError",
    "EpsteinExposedServerError",
    "EpsteinExposedValidationError",
    "Flight",
    "PaginatedResponse",
    "PaginationMeta",
    "Person",
    "PersonDetail",
    "PersonStats",
    "SearchResults",
]
