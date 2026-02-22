# Changelog

All notable changes to this project will be documented in this file.

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
