# Credits: Erwin Lejeune — 2026-02-22
"""Tests for the asynchronous AsyncEpsteinExposed client."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from epsteinexposed._constants import BASE_URL
from epsteinexposed.async_client import AsyncEpsteinExposed
from epsteinexposed.exceptions import (
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
)

from .conftest import FakeResponse, make_envelope

BASE = BASE_URL
MOCK_TARGET = "curl_cffi.requests.AsyncSession.get"


# ── Lifecycle ─────────────────────────────────────────────────


class TestAsyncLifecycle:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncEpsteinExposed(base_url=BASE) as c:
            assert c._base == BASE

    @pytest.mark.asyncio
    async def test_close(self):
        c = AsyncEpsteinExposed(base_url=BASE)
        await c.close()


# ── Persons ───────────────────────────────────────────────────


class TestAsyncPersons:
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        data = [{"id": 1, "name": "Test", "slug": "test"}]
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))
            result = await async_client.search_persons(q="Test")
            assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_get_person(self, async_client):
        person = {
            "data": {
                "id": 1,
                "name": "Jane Doe",
                "slug": "jane-doe",
                "bio": "A person",
                "aliases": [],
            }
        }
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=200, _json=person)
            result = await async_client.get_person("jane-doe")
            assert result.name == "Jane Doe"

    @pytest.mark.asyncio
    async def test_not_found(self, async_client):
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=404, _json=None, _text="Not Found")
            with pytest.raises(EpsteinExposedNotFoundError):
                await async_client.get_person("missing")


# ── Documents ─────────────────────────────────────────────────


class TestAsyncDocuments:
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        data = [{"id": "d1", "title": "Flight Log"}]
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))
            result = await async_client.search_documents(q="flight")
            assert len(result.data) == 1


# ── Flights ───────────────────────────────────────────────────


class TestAsyncFlights:
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        data = [
            {
                "id": 1,
                "origin": "TIST",
                "passengerNames": ["A"],
                "passengerIds": [1],
                "passengerCount": 1,
            }
        ]
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))
            result = await async_client.search_flights(passenger="A")
            assert result.data[0].origin == "TIST"


# ── Search ────────────────────────────────────────────────────


class TestAsyncSearch:
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        raw = {
            "status": "ok",
            "documents": {"results": [{"id": "d1"}]},
            "emails": {"results": []},
        }
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=200, _json=raw)
            result = await async_client.search(q="wexner")
            assert len(result.documents.results) == 1


# ── Errors ────────────────────────────────────────────────────


class TestAsyncErrors:
    @pytest.mark.asyncio
    async def test_rate_limit(self, async_client):
        with patch(MOCK_TARGET, new_callable=AsyncMock) as mock_get:
            mock_get.return_value = FakeResponse(status_code=429, _json=None, _text="Rate limited")
            with pytest.raises(EpsteinExposedRateLimitError):
                await async_client.search_persons()
