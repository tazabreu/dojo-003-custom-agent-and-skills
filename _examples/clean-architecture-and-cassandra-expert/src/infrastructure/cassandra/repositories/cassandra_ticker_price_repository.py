from datetime import datetime
from decimal import Decimal

from cassandra.cluster import Session

from src.domain.entities.ticker_price import TickerPrice


class CassandraTickerPriceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._insert_stmt = session.prepare(
            "INSERT INTO ticker_prices (ticker, ts, price, currency, source) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        self._select_stmt = session.prepare(
            "SELECT ticker, ts, price, currency, source FROM ticker_prices "
            "WHERE ticker = ?"
        )
        self._exists_stmt = session.prepare(
            "SELECT ticker FROM ticker_prices WHERE ticker = ? AND ts = ?"
        )

    def insert(self, entity: TickerPrice) -> None:
        self._session.execute(
            self._insert_stmt,
            (entity.ticker, entity.ts, entity.price, entity.currency, entity.source),
        )

    def get_by_ticker(
        self,
        ticker: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[TickerPrice]:
        if start or end:
            clauses = ["ticker = ?"]
            params: list[str | datetime] = [ticker]
            if start:
                clauses.append("ts >= ?")
                params.append(start)
            if end:
                clauses.append("ts <= ?")
                params.append(end)
            query = (
                "SELECT ticker, ts, price, currency, source FROM ticker_prices "
                f"WHERE {' AND '.join(clauses)}"
            )
            rows = self._session.execute(query, params)
        else:
            rows = self._session.execute(self._select_stmt, (ticker,))

        return [
            TickerPrice(
                ticker=row.ticker,
                ts=row.ts,
                price=Decimal(str(row.price)),
                currency=row.currency,
                source=row.source,
            )
            for row in rows
        ]

    def exists(self, ticker: str, ts: datetime) -> bool:
        result = self._session.execute(self._exists_stmt, (ticker, ts))
        return result.one() is not None
