"""
FR-001: Insert Ticker Price Data
=================================
Priority: P1
Refs: spec-kit FR style, OpenSpec propose/specs pattern

As a data consumer, I want to POST ticker price records
so that historical stock prices are persisted for later analysis.

Acceptance:
  - GIVEN a valid payload {ticker, price, timestamp}
    WHEN  POST /api/v1/ticker-prices
    THEN  201 Created is returned with the persisted record

  - GIVEN a valid payload with optional currency and source fields
    WHEN  POST /api/v1/ticker-prices
    THEN  201 Created is returned; defaults (USD, manual) are applied if omitted

  - GIVEN a duplicate (ticker, timestamp) combination already exists
    WHEN  POST /api/v1/ticker-prices
    THEN  409 Conflict is returned

  - GIVEN an invalid payload (missing required fields or negative price)
    WHEN  POST /api/v1/ticker-prices
    THEN  422 Unprocessable Entity is returned

Edge Cases:
  - Ticker symbols are normalized to uppercase (e.g. "aapl" -> "AAPL")
  - Prices must be strictly positive decimals
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.main import create_app

pytestmark = pytest.mark.functional


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


VALID_PAYLOAD = {
    "ticker": "AAPL",
    "price": "182.52",
    "timestamp": "2025-01-15T14:30:00Z",
}


class TestFR001InsertTickerPrice:
    """FR-001 acceptance scenarios."""

    async def test_insert_returns_201(self, client: AsyncClient):
        resp = await client.post("/api/v1/ticker-prices", json=VALID_PAYLOAD)
        assert resp.status_code == 201
        body = resp.json()
        assert body["ticker"] == "AAPL"
        assert body["price"] == "182.52" or float(body["price"]) == pytest.approx(182.52)

    async def test_defaults_applied_when_optional_fields_omitted(self, client: AsyncClient):
        payload = {"ticker": "GOOG", "price": "140.00", "timestamp": "2025-02-01T10:00:00Z"}
        resp = await client.post("/api/v1/ticker-prices", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["currency"] == "USD"
        assert body["source"] == "manual"

    async def test_duplicate_returns_409(self, client: AsyncClient):
        payload = {"ticker": "MSFT", "price": "400.00", "timestamp": "2025-03-01T09:00:00Z"}
        first = await client.post("/api/v1/ticker-prices", json=payload)
        assert first.status_code == 201

        second = await client.post("/api/v1/ticker-prices", json=payload)
        assert second.status_code == 409

    async def test_invalid_payload_returns_422(self, client: AsyncClient):
        resp = await client.post("/api/v1/ticker-prices", json={"ticker": "AAPL"})
        assert resp.status_code == 422

    async def test_negative_price_returns_422(self, client: AsyncClient):
        payload = {**VALID_PAYLOAD, "price": "-10.00", "ticker": "NEG1"}
        resp = await client.post("/api/v1/ticker-prices", json=payload)
        assert resp.status_code == 422

    async def test_ticker_normalized_to_uppercase(self, client: AsyncClient):
        payload = {**VALID_PAYLOAD, "ticker": "aapl", "timestamp": "2025-06-01T12:00:00Z"}
        resp = await client.post("/api/v1/ticker-prices", json=payload)
        assert resp.status_code == 201
        assert resp.json()["ticker"] == "AAPL"
