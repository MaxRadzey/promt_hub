import asyncpg


async def create_pool(
    dsn: str,
    min_size: int = 2,
    max_size: int = 10,
    timeout: float = 10.0,
    command_timeout: float = 30.0,
) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn,
        min_size=min_size,
        max_size=max_size,
        timeout=timeout,
        command_timeout=command_timeout,
    )
