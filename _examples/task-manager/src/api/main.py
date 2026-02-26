from fastapi import FastAPI

from src.api.routes import tasks


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Manager API",
        description="Simple task management service backed by Apache Cassandra",
        version="0.1.0",
    )
    app.include_router(tasks.router)
    return app


app = create_app()
