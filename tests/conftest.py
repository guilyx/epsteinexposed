# Credits: Erwin Lejeune — 2026-02-22
"""Shared test fixtures."""

from __future__ import annotations

import pytest

from epsteinexposed._constants import BASE_URL
from epsteinexposed.async_client import AsyncEpsteinExposed
from epsteinexposed.client import EpsteinExposed

BASE = BASE_URL


@pytest.fixture
def client():
    with EpsteinExposed(base_url=BASE) as c:
        yield c


@pytest.fixture
async def async_client():
    async with AsyncEpsteinExposed(base_url=BASE) as c:
        yield c


PAGINATED_ENVELOPE = {
    "status": "ok",
    "data": [],
    "meta": {"total": 0, "page": 1, "per_page": 20, "timestamp": "2026-02-22T00:00:00.000Z"},
}


def make_envelope(data: list, total: int | None = None, page: int = 1, per_page: int = 20):
    return {
        "status": "ok",
        "data": data,
        "meta": {
            "total": total if total is not None else len(data),
            "page": page,
            "per_page": per_page,
            "timestamp": "2026-02-22T00:00:00.000Z",
        },
    }
