"""Unit tests for the InsertTickerPrice use case."""

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from src.application.use_cases.insert_ticker_price import (
    DuplicateTickerPriceError,
    InsertTickerPrice,
)
from src.domain.entities.ticker_price import TickerPrice


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def use_case(repo):
    return InsertTickerPrice(repo)


@pytest.fixture
def sample_entity():
    return TickerPrice(
        ticker="AAPL",
        ts=datetime(2025, 1, 15, 14, 30, tzinfo=timezone.utc),
        price=Decimal("182.52"),
    )


class TestInsertTickerPrice:
    def test_inserts_new_entity(self, use_case, repo, sample_entity):
        repo.exists.return_value = False

        result = use_case.execute(sample_entity)

        repo.insert.assert_called_once_with(sample_entity)
        assert result == sample_entity

    def test_raises_on_duplicate(self, use_case, repo, sample_entity):
        repo.exists.return_value = True

        with pytest.raises(DuplicateTickerPriceError):
            use_case.execute(sample_entity)

        repo.insert.assert_not_called()
