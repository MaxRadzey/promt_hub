from contextlib import asynccontextmanager

from asyncpg.pool import Pool
from app.core.settings import Config

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await app.state.dishka_container.get(Pool)
    yield
    await app.state.dishka_container.close()


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title="Prompt Hub",
        description="API for storing and browsing prompts",
        version="0.1.0",
        lifespan=lifespan,
    )

    return app
