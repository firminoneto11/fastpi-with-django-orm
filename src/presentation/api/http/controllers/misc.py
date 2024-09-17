from fastapi import APIRouter

from src.app.services.misc import HealthCheckService
from src.infra.db import DBAdapter

resource_name = "health-check"
router = APIRouter()


@router.get("/health-check", name=f"{resource_name}:list")
async def health_check():
    svc = HealthCheckService(db=DBAdapter())
    return await svc()
