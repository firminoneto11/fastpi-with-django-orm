from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from fastapi import Request
    from rest_framework.exceptions import ValidationError


async def drf_validation_error_handler(request: "Request", exc: "ValidationError"):
    return JSONResponse(status_code=400, content=exc.detail)
