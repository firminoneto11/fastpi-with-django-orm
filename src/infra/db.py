from asgiref.sync import sync_to_async
from django.db import connection

from src.app.ports.outbound.db import DBPort


class DBAdapter(DBPort):
    @sync_to_async
    def ping(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            return True
        except:  # noqa
            return False
