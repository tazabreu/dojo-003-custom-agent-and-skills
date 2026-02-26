from datetime import datetime
from typing import Protocol

from src.domain.entities.ticker_price import TickerPrice


class TickerPriceRepository(Protocol):
    def insert(self, entity: TickerPrice) -> None: ...

    def get_by_ticker(
        self,
        ticker: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[TickerPrice]: ...

    def exists(self, ticker: str, ts: datetime) -> bool: ...
