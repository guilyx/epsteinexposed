# Credits: Erwin Lejeune — 2026-02-22
"""Pydantic models for all Epstein Exposed API response types."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


def _to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class _CamelModel(BaseModel):
    """Base model that accepts both camelCase (from API) and snake_case."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=_to_camel)


# ── Pagination ────────────────────────────────────────────────


class PaginationMeta(BaseModel):
    """Metadata returned in the `meta` envelope field."""

    total: int = 0
    page: int = 1
    per_page: int = 20
    timestamp: str | None = None


class PaginatedResponse(_CamelModel, Generic[T]):
    """Standard API response envelope."""

    status: str = "ok"
    data: list[T] = Field(default_factory=list)
    meta: PaginationMeta = Field(default_factory=PaginationMeta)


# ── Persons ───────────────────────────────────────────────────


class PersonStats(_CamelModel):
    """Aggregate counts for a person."""

    flights: int = 0
    documents: int = 0
    connections: int = 0
    emails: int = 0


class Person(_CamelModel):
    """Person record from the list/search endpoint."""

    id: int | str
    name: str
    slug: str
    category: str | None = None
    short_bio: str | None = None
    image_url: str | None = None
    stats: PersonStats = Field(default_factory=PersonStats)


class PersonDetail(Person):
    """Extended person record from the detail endpoint."""

    bio: str | None = None
    aliases: list[str] = Field(default_factory=list)
    black_book_entry: bool | None = None


# ── Documents ─────────────────────────────────────────────────


class Document(_CamelModel):
    """Document record."""

    id: int | str
    title: str
    date: str | None = None
    source: str | None = None
    category: str | None = None
    summary: str | None = None
    source_url: str | None = None
    tags: list[str] = Field(default_factory=list)


# ── Flights ───────────────────────────────────────────────────


class Flight(_CamelModel):
    """Flight log record."""

    id: int | str
    date: str | None = None
    origin: str | None = None
    destination: str | None = None
    aircraft: str | None = None
    pilot: str | None = None
    passenger_ids: list[int | str] = Field(default_factory=list)
    passenger_names: list[str] = Field(default_factory=list)
    passenger_count: int = 0


# ── Cross-type search ─────────────────────────────────────────


class _SearchBucket(BaseModel):
    results: list[dict[str, Any]] = Field(default_factory=list)


class SearchResults(BaseModel):
    """Response from the /search endpoint."""

    status: str = "ok"
    documents: _SearchBucket = Field(default_factory=_SearchBucket)
    emails: _SearchBucket = Field(default_factory=_SearchBucket)
