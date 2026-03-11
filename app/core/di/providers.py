from collections.abc import AsyncIterator

import asyncpg
from dishka import Provider, Scope, provide

from app.core.database.pool import create_pool
from app.core.settings import Config


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    async def get_pool(self, config: Config) -> AsyncIterator[asyncpg.Pool]:
        pool = await create_pool(
            config.db.dsn,
            min_size=config.db.pool_min_size,
            max_size=config.db.pool_max_size,
            timeout=config.db.connect_timeout,
            command_timeout=config.db.command_timeout,
        )
        yield pool
        await pool.close()

    @provide(scope=Scope.REQUEST)
    async def get_connection(self, pool: asyncpg.Pool) -> AsyncIterator[asyncpg.Connection]:
        async with pool.acquire() as conn:
            yield conn
