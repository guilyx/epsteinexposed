# Credits: Erwin Lejeune — 2026-02-22
"""Shared constants for the epsteinexposed package."""

from __future__ import annotations

BASE_URL = "https://epsteinexposed.com/api/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100
USER_AGENT = "epsteinexposed-python/0.1.0"

PERSON_CATEGORIES = frozenset(
    {
        "politician",
        "business",
        "royalty",
        "celebrity",
        "associate",
        "legal",
        "academic",
        "socialite",
        "military-intelligence",
        "other",
    }
)

DOCUMENT_SOURCES = frozenset(
    {
        "court-filing",
        "doj-release",
        "fbi",
        "efta",
    }
)

DOCUMENT_CATEGORIES = frozenset(
    {
        "deposition",
        "testimony",
        "correspondence",
    }
)

SEARCH_TYPES = frozenset({"documents", "emails"})
