# Exceptions

All exceptions inherit from `EpsteinExposedAPIError`.

## Hierarchy

```
EpsteinExposedAPIError (base)
├── EpsteinExposedValidationError   (400)
├── EpsteinExposedNotFoundError     (404)
├── EpsteinExposedRateLimitError    (429)
└── EpsteinExposedServerError       (5xx)
```

## EpsteinExposedAPIError

Base exception. All API-related errors inherit from this.

| Attribute | Type | Description |
|---|---|---|
| `message` | `str` | Human-readable error message |
| `status_code` | `int \| None` | HTTP status code |
| `response` | `dict \| None` | Raw error response body |

## EpsteinExposedValidationError

Raised for **400 Bad Request** — invalid or missing query parameters.

## EpsteinExposedNotFoundError

Raised for **404 Not Found** — the requested person/document does not exist.

## EpsteinExposedRateLimitError

Raised for **429 Too Many Requests** — rate limit exceeded. Back off and retry.

> **Rate Limits:** `/persons`, `/documents`, `/flights`: 60 req/min — `/search`: 30 req/min

## EpsteinExposedServerError

Raised for **5xx** server errors.

## Example

```python
from epsteinexposed import (
    EpsteinExposed,
    EpsteinExposedAPIError,
    EpsteinExposedNotFoundError,
    EpsteinExposedRateLimitError,
)

client = EpsteinExposed()

try:
    detail = client.get_person("unknown-slug")
except EpsteinExposedNotFoundError as e:
    print(f"Not found: {e.message}")
except EpsteinExposedRateLimitError:
    print("Rate limited")
except EpsteinExposedAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
```
