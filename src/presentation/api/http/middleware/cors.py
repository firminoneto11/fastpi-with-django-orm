from typing import TYPE_CHECKING

from fastapi.middleware.cors import CORSMiddleware

if TYPE_CHECKING:
    from django.conf import LazySettings


def get_cors_config(settings: "LazySettings"):
    return {
        "middleware_class": CORSMiddleware,
        "allow_origins": settings.ALLOWED_ORIGINS,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
