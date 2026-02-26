"""
FR-002: Query Ticker Price History
====================================
Priority: P1
Refs: spec-kit FR style, OpenSpec propose/specs pattern

As a data consumer, I want to GET historical prices for a ticker
so that I can analyze price trends over time.

Acceptance:
  - GIVEN prices exist for ticker "AAPL"
    WHEN  GET /api/v1/ticker-prices/AAPL
    THEN  200 OK with list of prices sorted newest-first, count included

  - GIVEN no prices exist for ticker "ZZZZ"
    WHEN  GET /api/v1/ticker-prices/ZZZZ
    THEN  200 OK with an empty list and count = 0

  - GIVEN prices exist across a date range
    WHEN  GET /api/v1/ticker-prices/AAPL?start=...&end=...
    THEN  200 OK with only prices within the specified range

  - GIVEN a lowercase ticker in the URL path
    WHEN  GET /api/v1/ticker-prices/aapl
    THEN  ticker is normalized to uppercase in the response

Edge Cases:
  - start without end returns all prices from start onward
  - end without start returns all prices up to end
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


async def _seed_prices(client: AsyncClient) -> None:
    """Insert a few prices for AAPL to test queries against."""
    for day, price in [("2025-01-10T10:00:00Z", "180.00"), ("2025-01-15T10:00:00Z", "182.50"),
                       ("2025-01-20T10:00:00Z", "185.00")]:
        await client.post(
            "/api/v1/ticker-prices",
            json={"ticker": "AAPL", "price": price, "timestamp": day},
        )


class TestFR002GetTickerPrices:
    """FR-002 acceptance scenarios."""

    async def test_returns_prices_for_ticker(self, client: AsyncClient):
        await _seed_prices(client)
        resp = await client.get("/api/v1/ticker-prices/AAPL")
        assert resp.status_code == 200
        body = resp.json()
        assert body["ticker"] == "AAPL"
        assert body["count"] >= 3
        assert len(body["prices"]) == body["count"]

    async def test_empty_result_for_unknown_ticker(self, client: AsyncClient):
        resp = await client.get("/api/v1/ticker-prices/ZZZZ")
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] == 0
        assert body["prices"] == []

    async def test_date_range_filter(self, client: AsyncClient):
        await _seed_prices(client)
        resp = await client.get(
            "/api/v1/ticker-prices/AAPL",
            params={"start": "2025-01-12T00:00:00Z", "end": "2025-01-18T00:00:00Z"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] >= 1
        for p in body["prices"]:
            assert "2025-01-12" <= p["timestamp"][:10] <= "2025-01-18"

    async def test_ticker_normalized_in_response(self, client: AsyncClient):
        resp = await client.get("/api/v1/ticker-prices/aapl")
        assert resp.status_code == 200
        assert resp.json()["ticker"] == "AAPL"
