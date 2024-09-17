from fastapi import APIRouter

from src.app.services.misc import HealthCheckService

router = APIRouter()


@router.get("/health-check")
async def health_check():
    svc = HealthCheckService()
    return await svc()
