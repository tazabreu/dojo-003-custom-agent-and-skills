from functools import lru_cache

from cassandra.cluster import Session

from src.application.use_cases.get_ticker_prices import GetTickerPrices
from src.application.use_cases.insert_ticker_price import InsertTickerPrice
from src.infrastructure.cassandra.repositories.cassandra_ticker_price_repository import (
    CassandraTickerPriceRepository,
)
from src.infrastructure.cassandra.session import create_session


@lru_cache
def get_cassandra_session() -> Session:
    return create_session()


def get_ticker_price_repo() -> CassandraTickerPriceRepository:
    return CassandraTickerPriceRepository(get_cassandra_session())


def get_insert_use_case() -> InsertTickerPrice:
    return InsertTickerPrice(get_ticker_price_repo())


def get_query_use_case() -> GetTickerPrices:
    return GetTickerPrices(get_ticker_price_repo())
