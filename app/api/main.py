from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api import routers
from app.api.application import create_app
from app.core.di.providers import DefaultProvider
from app.core.settings import Config


def start_app() -> FastAPI:
    config = Config()
    app = create_app(config)

    for router in routers:
        app.include_router(router)

    providers = [
        DefaultProvider(),
    ]
    container = make_async_container(*providers)
    setup_dishka(container, app)

    return app
