# AsyncEpsteinExposed (Async Client)

Asynchronous client using `httpx.AsyncClient`. Identical API to the sync client but all methods are `async`.

## Constructor

```python
AsyncEpsteinExposed(
    base_url: str = "https://epsteinexposed.com/api/v1",
    timeout: float = 30.0,
)
```

Supports use as an async context manager:

```python
async with AsyncEpsteinExposed() as client:
    ...
```

## Methods

All methods mirror `EpsteinExposed` but are coroutines:

```python
await client.search_persons(q="clinton")
await client.get_person("bill-clinton")
await client.search_documents(q="deposition")
await client.search_flights(passenger="maxwell")
await client.search(q="wexner trust")
await client.close()
```

See [Sync Client](client.md) for full parameter documentation.

## Example

```python
import asyncio
from epsteinexposed import AsyncEpsteinExposed

async def main():
    async with AsyncEpsteinExposed() as client:
        # Concurrent requests
        import asyncio as aio
        persons, docs, flights = await aio.gather(
            client.search_persons(q="maxwell"),
            client.search_documents(q="deposition"),
            client.search_flights(year=2002),
        )
        print(f"{persons.meta.total} persons")
        print(f"{docs.meta.total} documents")
        print(f"{flights.meta.total} flights")

asyncio.run(main())
```
