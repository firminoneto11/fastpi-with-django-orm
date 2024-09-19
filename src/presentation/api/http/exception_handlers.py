from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse
from rest_framework.exceptions import ValidationError

if TYPE_CHECKING:
    from fastapi import Request


async def drf_validation_error_handler(request: "Request", exc: ValidationError):
    return JSONResponse(status_code=400, content=exc.detail)


PAIRS = (
    {
        "exc": ValidationError,
        "handler": drf_validation_error_handler,
    },
)
