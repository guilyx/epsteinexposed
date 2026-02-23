# epsteinexposed

> Credits: Erwin Lejeune — 2026-02-22

[![CI](https://github.com/guilyx/epsteinexposed/actions/workflows/ci.yml/badge.svg)](https://github.com/guilyx/epsteinexposed/actions/workflows/ci.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8ea9be0e475e41a1aaa5f1a3f91c4c64)](https://app.codacy.com?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![codecov](https://codecov.io/gh/guilyx/epsteinexposed/graph/badge.svg)](https://codecov.io/gh/guilyx/epsteinexposed)
[![PyPI](https://img.shields.io/pypi/v/epsteinexposed)](https://pypi.org/project/epsteinexposed/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/epsteinexposed)](https://pypi.org/project/epsteinexposed/)
[![Python](https://img.shields.io/pypi/pyversions/epsteinexposed)](https://pypi.org/project/epsteinexposed/)
[![PyPI - Format](https://img.shields.io/pypi/format/epsteinexposed)](https://pypi.org/project/epsteinexposed/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-vite%20%2B%20react-blue)](https://guilyx.github.io/epsteinexposed)

**Unofficial Python client for the [Epstein Exposed](https://epsteinexposed.com) public API.**

Search persons, documents, flight logs, and emails from the Epstein case files — programmatically, with both sync and async interfaces.

> **Disclaimer:** Inclusion in the Epstein Exposed database does not imply guilt or wrongdoing. All data is derived from publicly released government records, court filings, and verified reporting. Attribution to [epsteinexposed.com](https://epsteinexposed.com) is requested.

## Installation

```bash
pip install epsteinexposed
```

## Quick Start

### Synchronous

```python
from epsteinexposed import EpsteinExposed

with EpsteinExposed() as client:
    # Search persons
    persons = client.search_persons(q="clinton", category="politician")
    for p in persons.data:
        print(f"{p.name} — {p.stats.flights} flights, {p.stats.documents} docs")

    # Get person detail
    detail = client.get_person("bill-clinton")
    print(detail.bio, detail.aliases)

    # Search documents
    docs = client.search_documents(q="little st james", source="court-filing")
    for d in docs.data:
        print(d.title, d.source_url)

    # Search flights
    flights = client.search_flights(passenger="trump", year=1997)
    for f in flights.data:
        print(f"{f.date}: {f.origin} → {f.destination}")

    # Cross-type search
    results = client.search(q="wexner trust", type="documents")
    print(len(results.documents.results), "document hits")
```

### Asynchronous

```python
import asyncio
from epsteinexposed import AsyncEpsteinExposed

async def main():
    async with AsyncEpsteinExposed() as client:
        persons = await client.search_persons(q="maxwell")
        for p in persons.data:
            print(p.name)

asyncio.run(main())
```

## Cloudflare & TLS Impersonation

The upstream API is behind Cloudflare bot protection, which blocks standard HTTP clients (`httpx`, `requests`) with a 403 challenge page. This library uses [`curl_cffi`](https://github.com/lexiforest/curl_cffi) to impersonate a Chrome browser's TLS fingerprint, bypassing the challenge transparently.

```python
client = EpsteinExposed(impersonate="chrome")  # default
```

## API Coverage

| Endpoint | Method | Client Method |
|---|---|---|
| `GET /api/v1/persons` | Search/filter persons | `search_persons()` |
| `GET /api/v1/persons/:slug` | Person detail | `get_person()` |
| `GET /api/v1/documents` | Search documents (FTS5) | `search_documents()` |
| `GET /api/v1/flights` | Search flight logs | `search_flights()` |
| `GET /api/v1/search` | Cross-type search | `search()` |

## Rate Limits

The upstream API enforces per-IP rate limits using a sliding window:

| Endpoints | Limit |
|---|---|
| `/persons`, `/persons/:slug`, `/documents`, `/flights` | 60 requests / minute |
| `/search` | 30 requests / minute |

Exceeding the limit returns HTTP 429 and raises `EpsteinExposedRateLimitError`.

## Response Models

All responses are parsed into typed Pydantic models:

- `PaginatedResponse[Person]`, `PaginatedResponse[Document]`, `PaginatedResponse[Flight]`
- `PersonDetail` (extended person with bio, aliases, black book status)
- `SearchResults` (documents + emails)
- `PaginationMeta` (total, page, per_page, timestamp)

## Error Handling

```python
from epsteinexposed import EpsteinExposed, EpsteinExposedRateLimitError

client = EpsteinExposed()
try:
    client.search_persons(q="test")
except EpsteinExposedRateLimitError:
    print("Rate limited — back off and retry")
```

| Exception | HTTP Code |
|---|---|
| `EpsteinExposedValidationError` | 400 |
| `EpsteinExposedNotFoundError` | 404 |
| `EpsteinExposedRateLimitError` | 429 |
| `EpsteinExposedServerError` | 5xx |
| `EpsteinExposedAPIError` | (base) |

## Development

```bash
git clone https://github.com/guilyx/epsteinexposed.git
cd epsteinexposed
make install-dev
make test          # unit tests (mocked)
make lint
```

Run integration tests against the real API (rate-limit aware):

```bash
pytest -m integration --no-cov
```

## Documentation

Full docs at [guilyx.github.io/epsteinexposed](https://guilyx.github.io/epsteinexposed) — built with Vite + React + Tailwind CSS. Run locally with `make docs`.

## License

MIT — see [LICENSE](LICENSE).
