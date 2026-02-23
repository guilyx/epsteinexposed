# Credits: Erwin Lejeune — 2026-02-22
"""Synchronous client for the Epstein Exposed public API.

Uses curl_cffi with browser TLS impersonation to bypass Cloudflare
bot protection on the upstream API.
"""

from __future__ import annotations

from typing import Any

from curl_cffi import requests as cf_requests

from epsteinexposed._constants import (
    BASE_URL,
    DEFAULT_IMPERSONATE,
    DEFAULT_PER_PAGE,
    DEFAULT_TIMEOUT,
)
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
    Person,
    PersonDetail,
    SearchResults,
)


class EpsteinExposed:
    """Synchronous client for the Epstein Exposed API.

    No authentication required. Attribution to epsteinexposed.com is requested.

    Uses browser TLS impersonation (via curl_cffi) to work with the
    Cloudflare-protected API.

    Example::

        from epsteinexposed import EpsteinExposed

        with EpsteinExposed() as client:
            persons = client.search_persons(q="clinton", category="politician")
            for p in persons.data:
                print(p.name, p.stats.flights)
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        impersonate: str = DEFAULT_IMPERSONATE,
    ) -> None:
        self._base = base_url.rstrip("/")
        self._http = cf_requests.Session(
            impersonate=impersonate,
            timeout=timeout,
        )

    # ── Lifecycle ─────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._http.close()

    def __enter__(self) -> EpsteinExposed:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ── Internal ──────────────────────────────────────────────

    def _request(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self._base}{path}"
        resp = self._http.get(url, params=params)
        if resp.status_code >= 400:
            self._raise_for_status(resp.status_code, resp)
        return resp.json()  # type: ignore[no-any-return]

    @staticmethod
    def _raise_for_status(code: int, resp: Any) -> None:
        body: dict[str, Any] | None = None
        try:
            body = resp.json()
        except Exception:
            pass

        msg = body.get("error", {}).get("message", f"HTTP {code}") if body else f"HTTP {code}"

        if code == 400:
            raise EpsteinExposedValidationError(msg, response=body)
        if code == 404:
            raise EpsteinExposedNotFoundError(msg, response=body)
        if code == 429:
            raise EpsteinExposedRateLimitError(msg, response=body)
        if code >= 500:
            raise EpsteinExposedServerError(msg, response=body)
        raise EpsteinExposedAPIError(msg, status_code=code, response=body)

    @staticmethod
    def _strip_none(params: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in params.items() if v is not None}

    # ── Persons ───────────────────────────────────────────────

    def search_persons(
        self,
        q: str | None = None,
        category: str | None = None,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> PaginatedResponse[Person]:
        """Search and filter persons of interest.

        Args:
            q: Search by name (partial or full).
            category: Filter by category (politician, business, royalty, ...).
            page: Page number (default 1).
            per_page: Results per page, max 100 (default 20).

        Returns:
            Paginated list of Person objects.
        """
        raw = self._request(
            "/persons",
            self._strip_none({"q": q, "category": category, "page": page, "per_page": per_page}),
        )
        return PaginatedResponse[Person](**raw)

    def get_person(self, slug: str) -> PersonDetail:
        """Retrieve a single person by their URL slug.

        Args:
            slug: URL slug (e.g. ``"bill-clinton"``).

        Returns:
            Full person detail including bio, aliases, and stats.
        """
        raw = self._request(f"/persons/{slug}")
        payload = raw.get("data", raw)
        return PersonDetail(**payload)

    # ── Documents ─────────────────────────────────────────────

    def search_documents(
        self,
        q: str | None = None,
        source: str | None = None,
        category: str | None = None,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> PaginatedResponse[Document]:
        """Search documents using full-text search.

        Args:
            q: FTS5 search query.
            source: Filter by source (court-filing, doj-release, fbi, efta).
            category: Filter by category (deposition, testimony, correspondence).
            page: Page number (default 1).
            per_page: Results per page, max 100 (default 20).

        Returns:
            Paginated list of Document objects.
        """
        raw = self._request(
            "/documents",
            self._strip_none(
                {
                    "q": q,
                    "source": source,
                    "category": category,
                    "page": page,
                    "per_page": per_page,
                }
            ),
        )
        return PaginatedResponse[Document](**raw)

    # ── Flights ───────────────────────────────────────────────

    def search_flights(
        self,
        passenger: str | None = None,
        year: int | None = None,
        origin: str | None = None,
        destination: str | None = None,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> PaginatedResponse[Flight]:
        """Search Epstein flight logs.

        Args:
            passenger: Filter by passenger name.
            year: Filter by year (e.g. 2002).
            origin: Filter by departure location.
            destination: Filter by arrival location.
            page: Page number (default 1).
            per_page: Results per page, max 100 (default 20).

        Returns:
            Paginated list of Flight objects.
        """
        raw = self._request(
            "/flights",
            self._strip_none(
                {
                    "passenger": passenger,
                    "year": year,
                    "origin": origin,
                    "destination": destination,
                    "page": page,
                    "per_page": per_page,
                }
            ),
        )
        return PaginatedResponse[Flight](**raw)

    # ── Cross-type search ─────────────────────────────────────

    def search(
        self,
        q: str,
        type: str | None = None,
        limit: int = DEFAULT_PER_PAGE,
    ) -> SearchResults:
        """Search across documents and emails simultaneously.

        Args:
            q: Search query (required).
            type: Limit to ``"documents"`` or ``"emails"``. Omit for both.
            limit: Max results per type, max 100 (default 20).

        Returns:
            SearchResults with document and email result buckets.
        """
        raw = self._request(
            "/search",
            self._strip_none({"q": q, "type": type, "limit": limit}),
        )
        return SearchResults(**raw)
