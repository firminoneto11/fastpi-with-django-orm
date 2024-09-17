from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from whitenoise import WhiteNoise  # type: ignore

from .controllers import misc_router

if TYPE_CHECKING:
    from django.conf import LazySettings


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI | WSGIMiddleware
    name: str


def _get_wsgi_app(settings: "LazySettings"):
    app = get_wsgi_application()
    app = WhiteNoise(app, settings.STATIC_ROOT, settings.STATIC_URL)

    return WSGIMiddleware(app=app)


def _get_app_v1(settings: "LazySettings"):
    app_v1 = FastAPI(**settings.GET_ASGI_SETTINGS())

    app_v1.include_router(misc_router)

    return app_v1


def get_mounts(settings: "LazySettings"):
    return [
        ApplicationMount(
            path=f"{settings.API_PATH}/v1",
            app=_get_app_v1(settings=settings),
            name="v1",
        ),
        ApplicationMount(
            path=f"{settings.ADMIN_PATH}",
            app=_get_wsgi_app(settings=settings),
            name="admin",
        ),
    ]
