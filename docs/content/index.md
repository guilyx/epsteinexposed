# epsteinexposed

**Unofficial Python client for the [Epstein Exposed](https://epsteinexposed.com) public API.**

Search persons, documents, flight logs, and emails from the Epstein case files — with both sync and async interfaces.

> **Disclaimer:** Inclusion in the Epstein Exposed database does not imply guilt or wrongdoing. All data is derived from publicly released government records, court filings, and verified reporting.

## Features

- **Sync + Async** — `EpsteinExposed` and `AsyncEpsteinExposed` clients
- **Cloudflare bypass** — Uses `curl_cffi` with browser TLS impersonation (the upstream API is behind Cloudflare bot protection)
- **Typed responses** — Pydantic v2 models for all API resources
- **Full API coverage** — Persons, Documents, Flights, Cross-type Search
- **Error hierarchy** — Granular exception classes mapped to HTTP status codes
- **Zero auth** — The upstream API requires no authentication

## Quick Example (Sync)

```python
from epsteinexposed import EpsteinExposed

with EpsteinExposed() as client:
    persons = client.search_persons(q="clinton", category="politician")
    for p in persons.data:
        print(p.name, p.stats.flights)
```

## Quick Example (Async)

```python
import asyncio
from epsteinexposed import AsyncEpsteinExposed

async def main():
    async with AsyncEpsteinExposed() as client:
        flights = await client.search_flights(passenger="maxwell")
        for f in flights.data:
            print(f"{f.date}: {f.origin} → {f.destination}")

asyncio.run(main())
```

## Installation

```bash
pip install epsteinexposed
```

## API Coverage

| Endpoint | Client Method |
|---|---|
| `GET /api/v1/persons` | `search_persons()` |
| `GET /api/v1/persons/:slug` | `get_person()` |
| `GET /api/v1/documents` | `search_documents()` |
| `GET /api/v1/flights` | `search_flights()` |
| `GET /api/v1/search` | `search()` |

## Rate Limits

The upstream API enforces per-IP rate limits using a sliding window:

| Endpoints | Limit |
|---|---|
| `/persons`, `/persons/:slug`, `/documents`, `/flights` | 60 requests / minute |
| `/search` | 30 requests / minute |

Exceeding the limit returns a `429` status and raises `EpsteinExposedRateLimitError`.
