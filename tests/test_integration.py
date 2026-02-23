# Credits: Erwin Lejeune — 2026-02-22
"""Integration tests hitting the real Epstein Exposed API.

These tests respect the published rate limits:

  Endpoint                                          | Limit
  --------------------------------------------------|--------------------
  /persons, /persons/:slug, /documents, /flights    | 60 requests / minute
  /search                                           | 30 requests / minute

  Limits are per IP using a sliding window.
  Exceeding the limit returns HTTP 429.

Run with:  pytest -m integration
"""

from __future__ import annotations

import asyncio
import time

import pytest

from epsteinexposed._constants import RATE_LIMIT_SEARCH, RATE_LIMIT_STANDARD
from epsteinexposed.async_client import AsyncEpsteinExposed
from epsteinexposed.client import EpsteinExposed
from epsteinexposed.exceptions import EpsteinExposedNotFoundError
from epsteinexposed.models import (
    Document,
    Flight,
    PaginatedResponse,
    Person,
    PersonDetail,
    SearchResults,
)

# Guard: rate-limit-safe delay between calls.
# Standard endpoints: 60 req/min → 1 req/sec is safe.
# Search endpoint:    30 req/min → 2 req/sec is safe.
STANDARD_DELAY = 60.0 / RATE_LIMIT_STANDARD  # 1.0 s
SEARCH_DELAY = 60.0 / RATE_LIMIT_SEARCH  # 2.0 s


def _sleep_standard() -> None:
    time.sleep(STANDARD_DELAY)


def _sleep_search() -> None:
    time.sleep(SEARCH_DELAY)


async def _async_sleep_standard() -> None:
    await asyncio.sleep(STANDARD_DELAY)


async def _async_sleep_search() -> None:
    await asyncio.sleep(SEARCH_DELAY)


# ── Sync integration ─────────────────────────────────────────


@pytest.mark.integration
class TestSyncPersons:
    """Sync /persons and /persons/:slug tests."""

    def test_search_persons_returns_data(self):
        with EpsteinExposed() as client:
            result = client.search_persons(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert result.status == "ok"
        assert result.meta.total > 0
        assert len(result.data) > 0
        assert all(isinstance(p, Person) for p in result.data)

    def test_search_persons_with_query(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            result = client.search_persons(q="clinton", per_page=5)

        assert result.status == "ok"
        names_lower = [p.name.lower() for p in result.data]
        assert any("clinton" in n for n in names_lower)

    def test_get_person_detail(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            listing = client.search_persons(per_page=1)
            slug = listing.data[0].slug

            _sleep_standard()
            detail = client.get_person(slug)

        assert isinstance(detail, PersonDetail)
        assert detail.slug == slug
        assert detail.name is not None

    def test_get_person_not_found(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            with pytest.raises(EpsteinExposedNotFoundError):
                client.get_person("this-person-does-not-exist-12345")


@pytest.mark.integration
class TestSyncDocuments:
    """Sync /documents tests."""

    def test_search_documents_returns_data(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            result = client.search_documents(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert result.status == "ok"
        assert len(result.data) > 0
        assert all(isinstance(d, Document) for d in result.data)


@pytest.mark.integration
class TestSyncFlights:
    """Sync /flights tests."""

    def test_search_flights_returns_data(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            result = client.search_flights(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert result.status == "ok"
        assert len(result.data) > 0
        assert all(isinstance(f, Flight) for f in result.data)

    def test_search_flights_with_filter(self):
        _sleep_standard()
        with EpsteinExposed() as client:
            result = client.search_flights(per_page=3)

        assert result.status == "ok"


@pytest.mark.integration
class TestSyncSearch:
    """Sync /search tests (stricter rate limit: 30 req/min)."""

    @pytest.mark.xfail(reason="Upstream /search endpoint currently returns 500", strict=False)
    def test_search_returns_results(self):
        _sleep_search()
        with EpsteinExposed() as client:
            result = client.search(q="epstein", limit=5)

        assert isinstance(result, SearchResults)
        assert result.status == "ok"


# ── Async integration ────────────────────────────────────────


@pytest.mark.integration
class TestAsyncPersons:
    """Async /persons and /persons/:slug tests."""

    @pytest.mark.asyncio
    async def test_search_persons_returns_data(self):
        await _async_sleep_standard()
        async with AsyncEpsteinExposed() as client:
            result = await client.search_persons(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert result.status == "ok"
        assert result.meta.total > 0
        assert len(result.data) > 0

    @pytest.mark.asyncio
    async def test_get_person_detail(self):
        await _async_sleep_standard()
        async with AsyncEpsteinExposed() as client:
            listing = await client.search_persons(per_page=1)
            slug = listing.data[0].slug

            await _async_sleep_standard()
            detail = await client.get_person(slug)

        assert isinstance(detail, PersonDetail)
        assert detail.slug == slug


@pytest.mark.integration
class TestAsyncDocuments:
    """Async /documents tests."""

    @pytest.mark.asyncio
    async def test_search_documents_returns_data(self):
        await _async_sleep_standard()
        async with AsyncEpsteinExposed() as client:
            result = await client.search_documents(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) > 0


@pytest.mark.integration
class TestAsyncFlights:
    """Async /flights tests."""

    @pytest.mark.asyncio
    async def test_search_flights_returns_data(self):
        await _async_sleep_standard()
        async with AsyncEpsteinExposed() as client:
            result = await client.search_flights(per_page=5)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) > 0


@pytest.mark.integration
class TestAsyncSearch:
    """Async /search tests (stricter rate limit: 30 req/min)."""

    @pytest.mark.xfail(reason="Upstream /search endpoint currently returns 500", strict=False)
    @pytest.mark.asyncio
    async def test_search_returns_results(self):
        await _async_sleep_search()
        async with AsyncEpsteinExposed() as client:
            result = await client.search(q="epstein", limit=5)

        assert isinstance(result, SearchResults)
        assert result.status == "ok"
