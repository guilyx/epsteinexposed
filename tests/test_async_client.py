# Credits: Erwin Lejeune — 2026-02-22
"""Tests for the asynchronous AsyncEpsteinExposed client."""

from __future__ import annotations

import pytest
import respx
from httpx import Response

from epsteinexposed._constants import BASE_URL
from epsteinexposed.async_client import AsyncEpsteinExposed
from epsteinexposed.exceptions import (
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
)

from .conftest import make_envelope

BASE = BASE_URL


# ── Lifecycle ─────────────────────────────────────────────────


class TestAsyncLifecycle:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncEpsteinExposed(base_url=BASE) as c:
            assert c._base == BASE
        assert c._http.is_closed

    @pytest.mark.asyncio
    async def test_close(self):
        c = AsyncEpsteinExposed(base_url=BASE)
        await c.close()
        assert c._http.is_closed


# ── Persons ───────────────────────────────────────────────────


class TestAsyncPersons:
    @respx.mock
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        data = [{"id": 1, "name": "Test", "slug": "test"}]
        respx.get(f"{BASE}/persons").mock(return_value=Response(200, json=make_envelope(data)))
        result = await async_client.search_persons(q="Test")
        assert len(result.data) == 1

    @respx.mock
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
        respx.get(f"{BASE}/persons/jane-doe").mock(return_value=Response(200, json=person))
        result = await async_client.get_person("jane-doe")
        assert result.name == "Jane Doe"

    @respx.mock
    @pytest.mark.asyncio
    async def test_not_found(self, async_client):
        respx.get(f"{BASE}/persons/missing").mock(return_value=Response(404))
        with pytest.raises(EpsteinExposedNotFoundError):
            await async_client.get_person("missing")


# ── Documents ─────────────────────────────────────────────────


class TestAsyncDocuments:
    @respx.mock
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        data = [{"id": "d1", "title": "Flight Log"}]
        respx.get(f"{BASE}/documents").mock(return_value=Response(200, json=make_envelope(data)))
        result = await async_client.search_documents(q="flight")
        assert len(result.data) == 1


# ── Flights ───────────────────────────────────────────────────


class TestAsyncFlights:
    @respx.mock
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
        respx.get(f"{BASE}/flights").mock(return_value=Response(200, json=make_envelope(data)))
        result = await async_client.search_flights(passenger="A")
        assert result.data[0].origin == "TIST"


# ── Search ────────────────────────────────────────────────────


class TestAsyncSearch:
    @respx.mock
    @pytest.mark.asyncio
    async def test_search(self, async_client):
        raw = {
            "status": "ok",
            "documents": {"results": [{"id": "d1"}]},
            "emails": {"results": []},
        }
        respx.get(f"{BASE}/search").mock(return_value=Response(200, json=raw))
        result = await async_client.search(q="wexner")
        assert len(result.documents.results) == 1


# ── Errors ────────────────────────────────────────────────────


class TestAsyncErrors:
    @respx.mock
    @pytest.mark.asyncio
    async def test_rate_limit(self, async_client):
        respx.get(f"{BASE}/persons").mock(return_value=Response(429))
        with pytest.raises(EpsteinExposedRateLimitError):
            await async_client.search_persons()
