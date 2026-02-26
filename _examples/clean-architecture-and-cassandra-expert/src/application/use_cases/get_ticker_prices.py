from datetime import datetime

from src.domain.entities.ticker_price import TickerPrice
from src.domain.repositories.ticker_price_repository import TickerPriceRepository


class GetTickerPrices:
    def __init__(self, repo: TickerPriceRepository) -> None:
        self._repo = repo

    def execute(
        self,
        ticker: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[TickerPrice]:
        return self._repo.get_by_ticker(ticker, start=start, end=end)
