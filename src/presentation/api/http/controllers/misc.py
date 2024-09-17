from fastapi import APIRouter, status

from src.app.services.misc import HealthCheckService
from src.infra.db import DBAdapter

resource_name = "health-check"
router = APIRouter()


@router.get(
    "/health-check",
    status_code=status.HTTP_200_OK,
    name=f"{resource_name}:list",
    summary="Pings the database and return if its alive or not",
)
async def health_check():
    svc = HealthCheckService(db=DBAdapter())
    return await svc()
