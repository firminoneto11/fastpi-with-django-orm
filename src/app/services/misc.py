from asgiref.sync import sync_to_async
from django.db import connection


class HealthCheckService:
    @sync_to_async
    def ping_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            return True
        except:  # noqa
            return False

    async def __call__(self):
        return {"healthy": await self.ping_database()}
