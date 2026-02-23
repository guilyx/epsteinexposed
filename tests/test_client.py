# Credits: Erwin Lejeune — 2026-02-22
"""Tests for the synchronous EpsteinExposed client."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from epsteinexposed._constants import BASE_URL
from epsteinexposed.client import EpsteinExposed
from epsteinexposed.exceptions import (
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
    EpsteinExposedServerError,
    EpsteinExposedValidationError,
)

from .conftest import FakeResponse, make_envelope

BASE = BASE_URL
MOCK_TARGET = "curl_cffi.requests.Session.get"


# ── Lifecycle ─────────────────────────────────────────────────


class TestLifecycle:
    def test_context_manager(self):
        with EpsteinExposed(base_url=BASE) as c:
            assert c._base == BASE

    def test_custom_base_url(self):
        c = EpsteinExposed(base_url="https://custom.api/v1/")
        assert c._base == "https://custom.api/v1"
        c.close()


# ── Persons ───────────────────────────────────────────────────


class TestSearchPersons:
    @patch(MOCK_TARGET)
    def test_basic(self, mock_get, client):
        data = [{"id": 1, "name": "Test", "slug": "test"}]
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))

        result = client.search_persons(q="Test")
        assert len(result.data) == 1
        assert result.data[0].name == "Test"

    @patch(MOCK_TARGET)
    def test_with_category(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope([]))
        client.search_persons(q="X", category="politician")
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["category"] == "politician"

    @patch(MOCK_TARGET)
    def test_pagination_params(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope([]))
        client.search_persons(page=3, per_page=50)
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["page"] == 3
        assert kwargs["params"]["per_page"] == 50

    @patch(MOCK_TARGET)
    def test_empty_results(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope([]))
        result = client.search_persons()
        assert result.data == []
        assert result.meta.total == 0


class TestGetPerson:
    @patch(MOCK_TARGET)
    def test_by_slug(self, mock_get, client):
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
        mock_get.return_value = FakeResponse(status_code=200, _json=person)
        result = client.get_person("bill-clinton")
        assert result.name == "Bill Clinton"
        assert result.black_book_entry is True
        assert result.stats.flights == 26

    @patch(MOCK_TARGET)
    def test_not_found(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=404, _json=None, _text="Not Found")
        with pytest.raises(EpsteinExposedNotFoundError):
            client.get_person("nobody")


# ── Documents ─────────────────────────────────────────────────


class TestSearchDocuments:
    @patch(MOCK_TARGET)
    def test_basic(self, mock_get, client):
        data = [{"id": "d1", "title": "Deposition", "source": "court-filing"}]
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))
        result = client.search_documents(q="deposition")
        assert len(result.data) == 1
        assert result.data[0].title == "Deposition"

    @patch(MOCK_TARGET)
    def test_filters(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope([]))
        client.search_documents(q="test", source="fbi", category="testimony")
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["source"] == "fbi"
        assert kwargs["params"]["category"] == "testimony"


# ── Flights ───────────────────────────────────────────────────


class TestSearchFlights:
    @patch(MOCK_TARGET)
    def test_basic(self, mock_get, client):
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
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope(data))
        result = client.search_flights(passenger="Doe")
        assert len(result.data) == 1
        assert result.data[0].origin == "Palm Beach"
        assert result.data[0].passenger_names == ["John Doe"]

    @patch(MOCK_TARGET)
    def test_filters(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=200, _json=make_envelope([]))
        client.search_flights(year=2003, origin="TIST")
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["year"] == 2003
        assert kwargs["params"]["origin"] == "TIST"


# ── Search ────────────────────────────────────────────────────


class TestSearch:
    @patch(MOCK_TARGET)
    def test_basic(self, mock_get, client):
        raw = {
            "status": "ok",
            "documents": {"results": [{"id": "d1", "title": "T"}]},
            "emails": {"results": []},
        }
        mock_get.return_value = FakeResponse(status_code=200, _json=raw)
        result = client.search(q="wexner")
        assert len(result.documents.results) == 1
        assert result.emails.results == []

    @patch(MOCK_TARGET)
    def test_type_filter(self, mock_get, client):
        mock_get.return_value = FakeResponse(
            status_code=200,
            _json={"status": "ok", "documents": {"results": []}, "emails": {"results": []}},
        )
        client.search(q="test", type="documents", limit=10)
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["type"] == "documents"
        assert kwargs["params"]["limit"] == 10


# ── Error handling ────────────────────────────────────────────


class TestErrors:
    @patch(MOCK_TARGET)
    def test_400(self, mock_get, client):
        mock_get.return_value = FakeResponse(
            status_code=400,
            _json={"status": "error", "error": {"message": "Bad param", "code": "BAD_REQUEST"}},
        )
        with pytest.raises(EpsteinExposedValidationError, match="Bad param"):
            client.search_persons()

    @patch(MOCK_TARGET)
    def test_429(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=429, _json=None, _text="Rate limited")
        with pytest.raises(EpsteinExposedRateLimitError):
            client.search_persons()

    @patch(MOCK_TARGET)
    def test_500(self, mock_get, client):
        mock_get.return_value = FakeResponse(status_code=500, _json=None, _text="Server error")
        with pytest.raises(EpsteinExposedServerError):
            client.search_persons()
