from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TickerPriceCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, examples=["AAPL"])
    price: Decimal = Field(..., gt=0, examples=[182.52])
    timestamp: datetime = Field(..., examples=["2025-01-15T14:30:00Z"])
    currency: str = Field(default="USD", max_length=3)
    source: str = Field(default="manual", max_length=50)


class TickerPriceResponse(BaseModel):
    ticker: str
    price: Decimal
    timestamp: datetime
    currency: str
    source: str


class TickerPriceListResponse(BaseModel):
    ticker: str
    count: int
    prices: list[TickerPriceResponse]
