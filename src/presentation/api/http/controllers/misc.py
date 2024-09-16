from asgiref.sync import sync_to_async
from django.db import connection
from fastapi import APIRouter

router = APIRouter()


@sync_to_async
def ping_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


@router.get("/health-check")
async def health_check():
    return {"healthy": await ping_database()}
