from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TickerPrice:
    ticker: str
    ts: datetime
    price: Decimal
    currency: str = "USD"
    source: str = "manual"
