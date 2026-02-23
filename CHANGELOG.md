# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] — 2026-02-23

### Fixed

- **Cloudflare 403 bypass** — Replaced `httpx` with `curl_cffi` for browser TLS impersonation; the upstream API is behind Cloudflare bot protection which rejects standard HTTP clients

### Changed

- HTTP transport: `httpx.Client` / `httpx.AsyncClient` → `curl_cffi.requests.Session` / `AsyncSession`
- New `impersonate` constructor parameter (default: `"chrome"`) controls the browser TLS profile
- Dependency: `httpx>=0.27.0` replaced by `curl_cffi>=0.14.0`
- Dev dependency `respx` removed (unit tests now use `unittest.mock.patch`)

### Added

- `RATE_LIMIT_STANDARD` (60 req/min) and `RATE_LIMIT_SEARCH` (30 req/min) constants
- 13 integration tests (`pytest -m integration`) hitting the real API with rate-limit-aware delays
- `FakeResponse` test helper for mocking `curl_cffi` responses
- CI integration test job (runs on `main` pushes only, with concurrency guard)
- Documentation for Cloudflare bypass, `impersonate` parameter, and rate limit tables

## [0.1.0] — 2026-02-22

### Added

- Synchronous `EpsteinExposed` client backed by `httpx.Client`
- Asynchronous `AsyncEpsteinExposed` client backed by `httpx.AsyncClient`
- Pydantic v2 models: `Person`, `PersonDetail`, `Document`, `Flight`, `SearchResults`, `PaginatedResponse[T]`, `PaginationMeta`, `PersonStats`
- Custom exception hierarchy mapped to HTTP status codes: `EpsteinExposedAPIError`, `ValidationError` (400), `NotFoundError` (404), `RateLimitError` (429), `ServerError` (5xx)
- Full API coverage: `search_persons`, `get_person`, `search_documents`, `search_flights`, `search`
- Context manager support for both sync (`with`) and async (`async with`) clients
- Comprehensive test suite with `pytest`, `pytest-asyncio`, and `respx` mocking
- CI workflow: ruff lint + format check, test matrix (Python 3.10–3.13), package build, Codecov upload
- PyPI publish workflow via GitHub Releases (trusted publishing)
- Vite + React 19 + Tailwind CSS 4 documentation site with typewriter cyberpunk theme
- Pre-commit hooks (ruff check + format)
- `Makefile` with `install`, `install-dev`, `test`, `lint`, `format`, `build`, `docs`, `clean` targets
