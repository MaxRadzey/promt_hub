import asyncpg
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status

from app.api.responses import (
    ErrorMessage,
    ErrorResponse,
    GeneralResponse,
    SuccessResponse,
    ValidationErrorItem,
)

technical_router = APIRouter(
    default_response_class=GeneralResponse,
    prefix="/technical",
    tags=["technical"],
    include_in_schema=False,
    route_class=DishkaRoute,
)


@technical_router.get(
    "/ping",
    summary="Проверка доступности API",
    description="Возвращает статус ok при работоспособности сервиса.",
    responses={
        status.HTTP_200_OK: {
            "description": "Сервис доступен.",
            "model": SuccessResponse[dict],
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации.",
            "model": ErrorResponse[ValidationErrorItem],
        },
    },
)
def ping() -> dict[str, str]:
    return {"status": "ok"}


@technical_router.get(
    "/db",
    summary="Проверка подключения к БД",
    description="Проверяет доступность базы данных.",
    responses={
        status.HTTP_200_OK: {
            "description": "БД доступна.",
            "model": SuccessResponse[dict],
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации.",
            "model": ErrorResponse[ValidationErrorItem],
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "БД недоступна.",
            "model": ErrorResponse[ErrorMessage],
        },
    },
)
async def db_health(pool: FromDishka[asyncpg.Pool]) -> dict[str, str]:
    """Проверка подключения к БД."""
    async with pool.acquire() as conn:
        await conn.fetchval("SELECT 1")
    return {"status": "ok", "database": "connected"}
