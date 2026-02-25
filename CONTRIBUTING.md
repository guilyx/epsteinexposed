# Contributing

Thanks for considering a contribution to **epsteinexposed**!

## Getting Started

```bash
git clone https://github.com/guilyx/epsteinexposed.git
cd epsteinexposed
make install-dev   # editable install + pre-commit hooks
```

## Development Workflow

| Command | Purpose |
|---|---|
| `make test` | Run unit tests (mocked, no network) |
| `make test-cov` | Unit tests with HTML coverage report |
| `make lint` | Ruff check + format verification |
| `make format` | Auto-fix lint issues and reformat |
| `make build` | Build sdist + wheel |
| `make docs` | Serve the docs site locally |
| `make clean` | Remove all build artifacts |

## Running Integration Tests

Integration tests hit the real [Epstein Exposed](https://epsteinexposed.com) API and are rate-limit aware. They are excluded from the default test run.

```bash
pytest -m integration --no-cov -v
```

> **Note:** The upstream API enforces 60 req/min on standard endpoints and 30 req/min on `/search`. The test suite inserts appropriate delays between calls.

## Code Standards

- **Python 3.10+** — use modern syntax (`X | Y` unions, etc.)
- **Ruff** — all code must pass `ruff check` and `ruff format --check`
- **Type hints** — all public APIs must be fully typed
- **Docstrings** — Google-style, with `Args:` and `Returns:` sections on public methods
- **Pydantic v2** — models use `ConfigDict` and `Field`, not v1 class-based config

Pre-commit hooks enforce linting and formatting automatically on each commit.

## Adding a New Endpoint

1. Add the method to `epsteinexposed/client.py` (sync) and `epsteinexposed/async_client.py` (async)
2. Add or reuse Pydantic models in `epsteinexposed/models.py`
3. Export new public symbols from `epsteinexposed/__init__.py`
4. Add unit tests in `tests/test_client.py` and `tests/test_async_client.py`
5. Add an integration test in `tests/test_integration.py`
6. Update the API Coverage table in `README.md`
7. Update `CHANGELOG.md` under an `[Unreleased]` section

## Submitting Changes

1. Fork the repo and create a feature branch from `main`
2. Make your changes — keep commits focused and well-described
3. Ensure `make lint` and `make test` pass
4. Open a pull request against `main`

## Releasing

Releases are managed by the maintainer:

1. Bump `version` in `pyproject.toml` and `epsteinexposed/_constants.py` (`USER_AGENT`)
2. Update `CHANGELOG.md` — move `[Unreleased]` items under a new version heading
3. Commit, push, and create a GitHub Release with tag `vX.Y.Z`
4. The `publish.yml` workflow handles PyPI publishing automatically

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
