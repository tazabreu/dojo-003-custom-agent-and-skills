from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_insert_use_case, get_query_use_case
from src.api.schemas.ticker_price import (
    TickerPriceCreate,
    TickerPriceListResponse,
    TickerPriceResponse,
)
from src.application.use_cases.get_ticker_prices import GetTickerPrices
from src.application.use_cases.insert_ticker_price import (
    DuplicateTickerPriceError,
    InsertTickerPrice,
)
from src.domain.entities.ticker_price import TickerPrice

router = APIRouter(prefix="/api/v1/ticker-prices", tags=["ticker-prices"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TickerPriceResponse)
def create_ticker_price(
    body: TickerPriceCreate,
    use_case: InsertTickerPrice = Depends(get_insert_use_case),
) -> TickerPriceResponse:
    entity = TickerPrice(
        ticker=body.ticker.upper(),
        ts=body.timestamp,
        price=body.price,
        currency=body.currency,
        source=body.source,
    )
    try:
        created = use_case.execute(entity)
    except DuplicateTickerPriceError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return TickerPriceResponse(
        ticker=created.ticker,
        price=created.price,
        timestamp=created.ts,
        currency=created.currency,
        source=created.source,
    )


@router.get("/{ticker}", response_model=TickerPriceListResponse)
def get_ticker_prices(
    ticker: str,
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    use_case: GetTickerPrices = Depends(get_query_use_case),
) -> TickerPriceListResponse:
    prices = use_case.execute(ticker.upper(), start=start, end=end)
    return TickerPriceListResponse(
        ticker=ticker.upper(),
        count=len(prices),
        prices=[
            TickerPriceResponse(
                ticker=p.ticker, price=p.price, timestamp=p.ts,
                currency=p.currency, source=p.source,
            )
            for p in prices
        ],
    )
