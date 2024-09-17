from dataclasses import dataclass

from src.app.ports.outbound.db import DBPort


@dataclass
class HealthCheckService:
    db: DBPort

    async def __call__(self):
        return {"healthy": await self.db.ping()}
