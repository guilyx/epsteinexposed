# Credits: Erwin Lejeune — 2026-02-22
"""Tests for Pydantic models."""

from __future__ import annotations

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


class TestPaginationMeta:
    def test_defaults(self):
        meta = PaginationMeta()
        assert meta.total == 0
        assert meta.page == 1
        assert meta.per_page == 20

    def test_from_dict(self):
        meta = PaginationMeta(total=42, page=3, per_page=10, timestamp="2026-01-01T00:00:00Z")
        assert meta.total == 42


class TestPerson:
    def test_camel_case_aliases(self):
        p = Person(
            id=1,
            name="John Doe",
            slug="john-doe",
            shortBio="A person",
            imageUrl="https://img.example.com/1.jpg",
        )
        assert p.short_bio == "A person"
        assert p.image_url == "https://img.example.com/1.jpg"

    def test_snake_case(self):
        p = Person(id=1, name="Jane", slug="jane", short_bio="Bio", image_url=None)
        assert p.short_bio == "Bio"

    def test_default_stats(self):
        p = Person(id=1, name="X", slug="x")
        assert p.stats.flights == 0


class TestPersonDetail:
    def test_extends_person(self):
        pd = PersonDetail(
            id=1,
            name="Test",
            slug="test",
            bio="Full bio",
            aliases=["T"],
            blackBookEntry=True,
        )
        assert pd.bio == "Full bio"
        assert pd.aliases == ["T"]
        assert pd.black_book_entry is True


class TestDocument:
    def test_camel_case(self):
        doc = Document(
            id="d1",
            title="Deposition",
            sourceUrl="https://example.com/d1",
        )
        assert doc.source_url == "https://example.com/d1"

    def test_defaults(self):
        doc = Document(id="d2", title="T")
        assert doc.tags == []
        assert doc.source is None


class TestFlight:
    def test_camel_case(self):
        f = Flight(
            id=1,
            passengerIds=[10, 20],
            passengerNames=["A", "B"],
            passengerCount=2,
        )
        assert f.passenger_ids == [10, 20]
        assert f.passenger_names == ["A", "B"]
        assert f.passenger_count == 2


class TestPersonStats:
    def test_defaults(self):
        s = PersonStats()
        assert s.flights == 0
        assert s.emails == 0


class TestPaginatedResponse:
    def test_empty(self):
        resp = PaginatedResponse[Person](
            status="ok",
            data=[],
            meta=PaginationMeta(),
        )
        assert resp.data == []
        assert resp.meta.total == 0

    def test_with_data(self):
        resp = PaginatedResponse[Person](
            status="ok",
            data=[{"id": 1, "name": "X", "slug": "x"}],
            meta={"total": 1, "page": 1, "per_page": 20},
        )
        assert len(resp.data) == 1
        assert resp.data[0].name == "X"


class TestSearchResults:
    def test_defaults(self):
        sr = SearchResults()
        assert sr.documents.results == []
        assert sr.emails.results == []

    def test_from_dict(self):
        sr = SearchResults(
            status="ok",
            documents={"results": [{"id": "d1", "title": "T"}]},
            emails={"results": []},
        )
        assert len(sr.documents.results) == 1
