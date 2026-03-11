from typing import Any, Generic, TypeVar

from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

ReponseT = TypeVar("ReponseT")
ErrorT = TypeVar("ErrorT", bound=BaseModel)


class SuccessResponse(BaseModel, Generic[ReponseT]):
    """Единый формат ответа API: errors, success, result."""

    errors: list[Any] = []
    success: bool = True
    result: ReponseT | None = None


class ErrorResponse(BaseModel, Generic[ErrorT]):
    """Единый формат ответа API: errors, success, result."""

    errors: list[ErrorT] = []
    success: bool = False


class ValidationErrorItem(BaseModel):
    """Элемент ошибки валидации для OpenAPI."""

    loc: list[str]
    msg: str
    type: str


class ErrorMessage(BaseModel):
    """Сообщение об ошибке для OpenAPI."""

    message: str


class GeneralResponse(ORJSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        payload = {"errors": [], "success": True, "result": content}
        return super().render(payload)
