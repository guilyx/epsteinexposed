# Getting Started

## Prerequisites

- **Python 3.10+**
- **pip** (or [uv](https://docs.astral.sh/uv/))

## Installation

```bash
pip install epsteinexposed
```

Or from source:

```bash
git clone https://github.com/guilyx/epsteinexposed.git
cd epsteinexposed
pip install -e ".[dev]"
```

## Your First Query

```python
from epsteinexposed import EpsteinExposed

client = EpsteinExposed()

# Search for persons
persons = client.search_persons(q="doe")
print(f"Found {persons.meta.total} persons")
for p in persons.data:
    print(f"  {p.name} ({p.category}) — {p.stats.documents} docs")

# Get person detail by slug
detail = client.get_person("bill-clinton")
print(detail.bio)
print("Aliases:", detail.aliases)

# Search documents
docs = client.search_documents(q="flight log", source="court-filing")
for d in docs.data:
    print(f"  {d.title} [{d.source}]")

# Search flights
flights = client.search_flights(passenger="clinton", year=2002)
for f in flights.data:
    print(f"  {f.date}: {f.origin} → {f.destination} ({f.passenger_count} pax)")

# Cross-type search
results = client.search(q="wexner trust")
print(f"{len(results.documents.results)} docs, {len(results.emails.results)} emails")

client.close()
```

## Using the Async Client

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

The upstream API is protected by Cloudflare bot detection, which blocks standard HTTP clients (`httpx`, `requests`, `urllib3`) with a 403 challenge page. This library uses [`curl_cffi`](https://github.com/lexiforest/curl_cffi) to impersonate a Chrome browser's TLS fingerprint, bypassing the challenge transparently.

You can control which browser profile is impersonated:

```python
client = EpsteinExposed(impersonate="chrome")      # default
client = EpsteinExposed(impersonate="safari")       # alternative
```

## Error Handling

```python
from epsteinexposed import (
    EpsteinExposed,
    EpsteinExposedRateLimitError,
    EpsteinExposedNotFoundError,
)

client = EpsteinExposed()

try:
    detail = client.get_person("nonexistent-slug")
except EpsteinExposedNotFoundError:
    print("Person not found")
except EpsteinExposedRateLimitError:
    print("Rate limited — wait and retry")
```

## Rate Limits

The upstream API enforces rate limits per IP address using a sliding window:

| Endpoints | Limit |
|---|---|
| `/persons`, `/persons/:slug`, `/documents`, `/flights` | 60 requests / minute |
| `/search` | 30 requests / minute |

A `429` response raises `EpsteinExposedRateLimitError`.

## Next Steps

- Browse the [source on GitHub](https://github.com/guilyx/epsteinexposed) for the full client, model, and exception APIs
- Read the [CHANGELOG](https://github.com/guilyx/epsteinexposed/blob/main/CHANGELOG.md) for version history
- See [Deployment](deployment.md) for publishing and docs hosting guides
