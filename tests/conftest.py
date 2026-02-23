# Credits: Erwin Lejeune — 2026-02-22
"""Shared test fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

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


@dataclass
class FakeResponse:
    """Mimics the curl_cffi response object for unit tests."""

    status_code: int = 200
    _json: dict[str, Any] | None = None
    _text: str = ""
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)

    def json(self) -> Any:
        if self._json is not None:
            return self._json
        return json.loads(self._text)

    @property
    def text(self) -> str:
        if self._json is not None:
            return json.dumps(self._json)
        return self._text
