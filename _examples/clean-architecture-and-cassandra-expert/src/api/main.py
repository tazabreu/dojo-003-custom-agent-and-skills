from fastapi import FastAPI

from src.api.routes import ticker_prices


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ticker Price API",
        description="Insert and query historical stock ticker prices (Cassandra-backed)",
        version="0.1.0",
    )
    app.include_router(ticker_prices.router)
    return app


app = create_app()
