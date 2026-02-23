# EpsteinExposed (Sync Client)

Synchronous client using `curl_cffi.requests.Session` with browser TLS impersonation to bypass Cloudflare bot protection.

## Constructor

```python
EpsteinExposed(
    base_url: str = "https://epsteinexposed.com/api/v1",
    timeout: float = 30.0,
    impersonate: str = "chrome",
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `base_url` | `str` | `https://epsteinexposed.com/api/v1` | API base URL |
| `timeout` | `float` | `30.0` | HTTP timeout in seconds |
| `impersonate` | `str` | `"chrome"` | Browser TLS profile to impersonate |

Supports use as a context manager:

```python
with EpsteinExposed() as client:
    ...
```

## Methods

### `search_persons(q, category, page, per_page)`

Search and filter persons of interest.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | `str \| None` | `None` | Name search query |
| `category` | `str \| None` | `None` | Category filter |
| `page` | `int` | `1` | Page number |
| `per_page` | `int` | `20` | Results per page (max 100) |

**Returns:** `PaginatedResponse[Person]`

### `get_person(slug)`

Retrieve a single person by URL slug.

| Parameter | Type | Description |
|---|---|---|
| `slug` | `str` | Person slug (e.g. `"bill-clinton"`) |

**Returns:** `PersonDetail`

**Raises:** `EpsteinExposedNotFoundError` if not found.

### `search_documents(q, source, category, page, per_page)`

Search documents using FTS5 full-text search.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | `str \| None` | `None` | Full-text search query |
| `source` | `str \| None` | `None` | Source filter |
| `category` | `str \| None` | `None` | Category filter |
| `page` | `int` | `1` | Page number |
| `per_page` | `int` | `20` | Results per page (max 100) |

**Returns:** `PaginatedResponse[Document]`

### `search_flights(passenger, year, origin, destination, page, per_page)`

Search Epstein flight logs.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `passenger` | `str \| None` | `None` | Passenger name |
| `year` | `int \| None` | `None` | Year filter |
| `origin` | `str \| None` | `None` | Departure location |
| `destination` | `str \| None` | `None` | Arrival location |
| `page` | `int` | `1` | Page number |
| `per_page` | `int` | `20` | Results per page (max 100) |

**Returns:** `PaginatedResponse[Flight]`

### `search(q, type, limit)`

Cross-type search across documents and emails.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | `str` | — | Search query (required) |
| `type` | `str \| None` | `None` | `"documents"` or `"emails"` |
| `limit` | `int` | `20` | Max results per type (max 100) |

**Returns:** `SearchResults`

### `close()`

Close the underlying HTTP session.
