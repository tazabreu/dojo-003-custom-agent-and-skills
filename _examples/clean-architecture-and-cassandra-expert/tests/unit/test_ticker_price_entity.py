"""Unit tests for the TickerPrice domain entity."""

from datetime import datetime, timezone
from decimal import Decimal

from src.domain.entities.ticker_price import TickerPrice


class TestTickerPriceEntity:
    def test_defaults(self):
        tp = TickerPrice(
            ticker="MSFT",
            ts=datetime(2025, 6, 1, tzinfo=timezone.utc),
            price=Decimal("420.00"),
        )
        assert tp.currency == "USD"
        assert tp.source == "manual"

    def test_is_frozen(self):
        tp = TickerPrice(
            ticker="MSFT",
            ts=datetime(2025, 6, 1, tzinfo=timezone.utc),
            price=Decimal("420.00"),
        )
        try:
            tp.ticker = "AAPL"  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def test_equality(self):
        kwargs = dict(
            ticker="GOOG",
            ts=datetime(2025, 3, 1, tzinfo=timezone.utc),
            price=Decimal("150.00"),
        )
        assert TickerPrice(**kwargs) == TickerPrice(**kwargs)
