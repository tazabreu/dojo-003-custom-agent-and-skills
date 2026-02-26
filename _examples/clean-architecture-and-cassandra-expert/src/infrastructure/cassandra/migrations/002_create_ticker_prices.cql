-- Migration: 002_create_ticker_prices
-- Description: Creates the ticker_prices table for storing historical stock data.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS ticker_data.ticker_prices (
    ticker    text,
    ts        timestamp,
    price     decimal,
    currency  text,
    source    text,
    PRIMARY KEY (ticker, ts)
) WITH CLUSTERING ORDER BY (ts DESC)
  AND comment = 'Historical ticker price data, partitioned by ticker, sorted newest-first';
