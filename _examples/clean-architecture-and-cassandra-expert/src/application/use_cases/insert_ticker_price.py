from src.domain.entities.ticker_price import TickerPrice
from src.domain.repositories.ticker_price_repository import TickerPriceRepository


class DuplicateTickerPriceError(Exception):
    def __init__(self, ticker: str, ts: str) -> None:
        super().__init__(f"Ticker price already exists: {ticker} @ {ts}")
        self.ticker = ticker
        self.ts = ts


class InsertTickerPrice:
    def __init__(self, repo: TickerPriceRepository) -> None:
        self._repo = repo

    def execute(self, entity: TickerPrice) -> TickerPrice:
        if self._repo.exists(entity.ticker, entity.ts):
            raise DuplicateTickerPriceError(entity.ticker, str(entity.ts))
        self._repo.insert(entity)
        return entity
