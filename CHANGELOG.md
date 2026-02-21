# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] — 2026-02-22

### Added

- Synchronous `EpsteinExposed` client (httpx)
- Asynchronous `AsyncEpsteinExposed` client (httpx)
- Pydantic models for Persons, Documents, Flights, and Search
- Custom exception hierarchy with status-code mapping
- Full test suite (sync + async) with respx mocking
- CI workflow (lint, test matrix 3.10-3.13, build)
- PyPI publish workflow (trusted publishing on GitHub release)
- MkDocs Material documentation site
- Pre-commit hooks (ruff)
