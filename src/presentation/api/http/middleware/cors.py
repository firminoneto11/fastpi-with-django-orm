from django.conf import settings
from fastapi.middleware.cors import CORSMiddleware

cors_middleware_configuration = {
    "middleware_class": CORSMiddleware,
    "allow_origins": settings.ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
