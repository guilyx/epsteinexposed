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

The upstream API enforces rate limits per IP:

| Endpoints | Limit |
|---|---|
| `/persons`, `/documents`, `/flights` | 60 req/min |
| `/search` | 30 req/min |

A `429` response raises `EpsteinExposedRateLimitError`.

## Next Steps

- [Sync Client API](api/client.md)
- [Async Client API](api/async-client.md)
- [Models Reference](api/models.md)
- [Error Handling](api/exceptions.md)
