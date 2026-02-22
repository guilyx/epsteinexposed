# Credits: Erwin Lejeune — 2026-02-22
"""Tests for the synchronous EpsteinExposed client."""

from __future__ import annotations

import pytest
import respx
from httpx import Response

from epsteinexposed._constants import BASE_URL
from epsteinexposed.client import EpsteinExposed
from epsteinexposed.exceptions import (
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
    EpsteinExposedServerError,
    EpsteinExposedValidationError,
)

from .conftest import make_envelope

BASE = BASE_URL


# ── Lifecycle ─────────────────────────────────────────────────


class TestLifecycle:
    def test_context_manager(self):
        with EpsteinExposed(base_url=BASE) as c:
            assert c._base == BASE
        assert c._http.is_closed

    def test_close(self):
        c = EpsteinExposed(base_url=BASE)
        c.close()
        assert c._http.is_closed

    def test_custom_base_url(self):
        c = EpsteinExposed(base_url="https://custom.api/v1/")
        assert c._base == "https://custom.api/v1"
        c.close()


# ── Persons ───────────────────────────────────────────────────


class TestSearchPersons:
    @respx.mock
    def test_basic(self, client):
        data = [{"id": 1, "name": "Test", "slug": "test"}]
        respx.get(f"{BASE}/persons").mock(return_value=Response(200, json=make_envelope(data)))

        result = client.search_persons(q="Test")
        assert len(result.data) == 1
        assert result.data[0].name == "Test"

    @respx.mock
    def test_with_category(self, client):
        route = respx.get(f"{BASE}/persons").mock(
            return_value=Response(200, json=make_envelope([]))
        )
        client.search_persons(q="X", category="politician")
        assert route.calls.last.request.url.params["category"] == "politician"

    @respx.mock
    def test_pagination_params(self, client):
        route = respx.get(f"{BASE}/persons").mock(
            return_value=Response(200, json=make_envelope([]))
        )
        client.search_persons(page=3, per_page=50)
        assert route.calls.last.request.url.params["page"] == "3"
        assert route.calls.last.request.url.params["per_page"] == "50"

    @respx.mock
    def test_empty_results(self, client):
        respx.get(f"{BASE}/persons").mock(return_value=Response(200, json=make_envelope([])))
        result = client.search_persons()
        assert result.data == []
        assert result.meta.total == 0


class TestGetPerson:
    @respx.mock
    def test_by_slug(self, client):
        person = {
            "data": {
                "id": 1,
                "name": "Bill Clinton",
                "slug": "bill-clinton",
                "category": "politician",
                "bio": "42nd President",
                "aliases": ["William Jefferson Clinton"],
                "blackBookEntry": True,
                "stats": {"flights": 26, "documents": 50, "connections": 10, "emails": 5},
            }
        }
        respx.get(f"{BASE}/persons/bill-clinton").mock(return_value=Response(200, json=person))
        result = client.get_person("bill-clinton")
        assert result.name == "Bill Clinton"
        assert result.black_book_entry is True
        assert result.stats.flights == 26

    @respx.mock
    def test_not_found(self, client):
        respx.get(f"{BASE}/persons/nobody").mock(return_value=Response(404))
        with pytest.raises(EpsteinExposedNotFoundError):
            client.get_person("nobody")


# ── Documents ─────────────────────────────────────────────────


class TestSearchDocuments:
    @respx.mock
    def test_basic(self, client):
        data = [{"id": "d1", "title": "Deposition", "source": "court-filing"}]
        respx.get(f"{BASE}/documents").mock(return_value=Response(200, json=make_envelope(data)))
        result = client.search_documents(q="deposition")
        assert len(result.data) == 1
        assert result.data[0].title == "Deposition"

    @respx.mock
    def test_filters(self, client):
        route = respx.get(f"{BASE}/documents").mock(
            return_value=Response(200, json=make_envelope([]))
        )
        client.search_documents(q="test", source="fbi", category="testimony")
        params = route.calls.last.request.url.params
        assert params["source"] == "fbi"
        assert params["category"] == "testimony"


# ── Flights ───────────────────────────────────────────────────


class TestSearchFlights:
    @respx.mock
    def test_basic(self, client):
        data = [
            {
                "id": 1,
                "date": "2002-01-15",
                "origin": "Palm Beach",
                "destination": "Teterboro",
                "passengerNames": ["John Doe"],
                "passengerIds": [10],
                "passengerCount": 1,
            }
        ]
        respx.get(f"{BASE}/flights").mock(return_value=Response(200, json=make_envelope(data)))
        result = client.search_flights(passenger="Doe")
        assert len(result.data) == 1
        assert result.data[0].origin == "Palm Beach"
        assert result.data[0].passenger_names == ["John Doe"]

    @respx.mock
    def test_filters(self, client):
        route = respx.get(f"{BASE}/flights").mock(
            return_value=Response(200, json=make_envelope([]))
        )
        client.search_flights(year=2003, origin="TIST")
        params = route.calls.last.request.url.params
        assert params["year"] == "2003"
        assert params["origin"] == "TIST"


# ── Search ────────────────────────────────────────────────────


class TestSearch:
    @respx.mock
    def test_basic(self, client):
        raw = {
            "status": "ok",
            "documents": {"results": [{"id": "d1", "title": "T"}]},
            "emails": {"results": []},
        }
        respx.get(f"{BASE}/search").mock(return_value=Response(200, json=raw))
        result = client.search(q="wexner")
        assert len(result.documents.results) == 1
        assert result.emails.results == []

    @respx.mock
    def test_type_filter(self, client):
        route = respx.get(f"{BASE}/search").mock(
            return_value=Response(
                200,
                json={"status": "ok", "documents": {"results": []}, "emails": {"results": []}},
            )
        )
        client.search(q="test", type="documents", limit=10)
        params = route.calls.last.request.url.params
        assert params["type"] == "documents"
        assert params["limit"] == "10"


# ── Error handling ────────────────────────────────────────────


class TestErrors:
    @respx.mock
    def test_400(self, client):
        respx.get(f"{BASE}/persons").mock(
            return_value=Response(
                400,
                json={"status": "error", "error": {"message": "Bad param", "code": "BAD_REQUEST"}},
            )
        )
        with pytest.raises(EpsteinExposedValidationError, match="Bad param"):
            client.search_persons()

    @respx.mock
    def test_429(self, client):
        respx.get(f"{BASE}/persons").mock(return_value=Response(429))
        with pytest.raises(EpsteinExposedRateLimitError):
            client.search_persons()

    @respx.mock
    def test_500(self, client):
        respx.get(f"{BASE}/persons").mock(return_value=Response(500))
        with pytest.raises(EpsteinExposedServerError):
            client.search_persons()
