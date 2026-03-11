import asyncio

import asyncpg
import pytest
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api.application import create_app
from app.core.di.providers import DefaultProvider
from app.core.settings import Config


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()


@pytest.fixture(scope="session")
async def container(config: Config):
    cont = make_async_container(DefaultProvider())
    yield cont
    await cont.close()


@pytest.fixture(scope="session")
async def pool(container):
    async with container():
        yield await container.get(asyncpg.Pool)


@pytest.fixture(scope="session")
def app(config: Config, container: AsyncContainer):
    from app.api import routers

    app = create_app(config)

    for router in routers:
        app.include_router(router)

    setup_dishka(container, app)
    return app


@pytest.fixture(scope="session")
async def test_client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
