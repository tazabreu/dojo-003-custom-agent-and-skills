"""Unit tests for the GetTickerPrices use case."""

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from src.application.use_cases.get_ticker_prices import GetTickerPrices
from src.domain.entities.ticker_price import TickerPrice


@pytest.fixture
def repo():
    mock = MagicMock()
    mock.get_by_ticker.return_value = [
        TickerPrice(
            ticker="AAPL",
            ts=datetime(2025, 1, 15, 14, 30, tzinfo=timezone.utc),
            price=Decimal("182.52"),
        ),
        TickerPrice(
            ticker="AAPL",
            ts=datetime(2025, 1, 14, 14, 30, tzinfo=timezone.utc),
            price=Decimal("181.00"),
        ),
    ]
    return mock


@pytest.fixture
def use_case(repo):
    return GetTickerPrices(repo)


class TestGetTickerPrices:
    def test_returns_prices_for_ticker(self, use_case, repo):
        result = use_case.execute("AAPL")

        repo.get_by_ticker.assert_called_once_with("AAPL", start=None, end=None)
        assert len(result) == 2
        assert all(p.ticker == "AAPL" for p in result)

    def test_passes_date_range(self, use_case, repo):
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        end = datetime(2025, 1, 31, tzinfo=timezone.utc)

        use_case.execute("AAPL", start=start, end=end)

        repo.get_by_ticker.assert_called_once_with("AAPL", start=start, end=end)
