import asyncpg
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter

technical_router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    include_in_schema=False,
)


@technical_router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


@technical_router.get("/db")
async def db_health(pool: FromDishka[asyncpg.Pool]) -> dict[str, str]:
    """Проверка подключения к БД."""
    async with pool.acquire() as conn:
        await conn.fetchval("SELECT 1")
    return {"status": "ok", "database": "connected"}
