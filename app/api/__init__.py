from fastapi import APIRouter

from app.api.technical.router import technical_router

api_router = APIRouter(prefix="/api")
# api_router.include_router(technical_router)

routers = (api_router, technical_router)

__all__ = ["routers"]
