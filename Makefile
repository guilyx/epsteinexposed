.PHONY: help install install-dev test test-cov lint format clean build docs

help:
	@echo "Available commands:"
	@echo "  make install       Install the package"
	@echo "  make install-dev   Install with dev + docs dependencies"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with HTML coverage report"
	@echo "  make lint          Run linters (ruff, mypy)"
	@echo "  make format        Auto-format code"
	@echo "  make clean         Remove build artefacts"
	@echo "  make build         Build sdist + wheel"
	@echo "  make docs          Serve docs locally"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs]"
	pre-commit install

test:
	pytest -m "not integration"

test-cov:
	pytest -m "not integration" --cov=epsteinexposed --cov-report=html --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .
	mypy epsteinexposed

format:
	ruff check --fix .
	ruff format .

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov/ coverage.xml site/
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true

build:
	python -m build

docs:
	mkdocs serve
