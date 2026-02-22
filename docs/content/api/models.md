# Models

All API responses are parsed into typed Pydantic v2 models. Field names use snake_case in Python; the library handles camelCase conversion from the API automatically.

## PaginationMeta

| Field | Type | Description |
|---|---|---|
| `total` | `int` | Total results across all pages |
| `page` | `int` | Current page number |
| `per_page` | `int` | Results per page |
| `timestamp` | `str \| None` | Server timestamp |

## PaginatedResponse[T]

Generic envelope returned by list endpoints.

| Field | Type | Description |
|---|---|---|
| `status` | `str` | `"ok"` on success |
| `data` | `list[T]` | List of typed objects |
| `meta` | `PaginationMeta` | Pagination metadata |

## PersonStats

| Field | Type |
|---|---|
| `flights` | `int` |
| `documents` | `int` |
| `connections` | `int` |
| `emails` | `int` |

## Person

Returned by `search_persons()`.

| Field | Type | API Alias |
|---|---|---|
| `id` | `int \| str` | `id` |
| `name` | `str` | `name` |
| `slug` | `str` | `slug` |
| `category` | `str \| None` | `category` |
| `short_bio` | `str \| None` | `shortBio` |
| `image_url` | `str \| None` | `imageUrl` |
| `stats` | `PersonStats` | `stats` |

## PersonDetail

Extends `Person`. Returned by `get_person()`.

| Extra Field | Type | API Alias |
|---|---|---|
| `bio` | `str \| None` | `bio` |
| `aliases` | `list[str]` | `aliases` |
| `black_book_entry` | `bool \| None` | `blackBookEntry` |

## Document

| Field | Type | API Alias |
|---|---|---|
| `id` | `int \| str` | `id` |
| `title` | `str` | `title` |
| `date` | `str \| None` | `date` |
| `source` | `str \| None` | `source` |
| `category` | `str \| None` | `category` |
| `summary` | `str \| None` | `summary` |
| `source_url` | `str \| None` | `sourceUrl` |
| `tags` | `list[str]` | `tags` |

## Flight

| Field | Type | API Alias |
|---|---|---|
| `id` | `int \| str` | `id` |
| `date` | `str \| None` | `date` |
| `origin` | `str \| None` | `origin` |
| `destination` | `str \| None` | `destination` |
| `aircraft` | `str \| None` | `aircraft` |
| `pilot` | `str \| None` | `pilot` |
| `passenger_ids` | `list[int \| str]` | `passengerIds` |
| `passenger_names` | `list[str]` | `passengerNames` |
| `passenger_count` | `int` | `passengerCount` |

## SearchResults

Returned by `search()`.

| Field | Type |
|---|---|
| `status` | `str` |
| `documents.results` | `list[dict]` |
| `emails.results` | `list[dict]` |
