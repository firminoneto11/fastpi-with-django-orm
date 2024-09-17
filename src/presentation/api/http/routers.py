from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from .controllers import misc_router

if TYPE_CHECKING:
    from django.conf import LazySettings


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI | WSGIMiddleware | StaticFiles
    name: str


def _get_wsgi_app(settings: "LazySettings"):
    app = get_wsgi_application()
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
        # NOTE: Django Admin site mounts
        ApplicationMount(
            path=f"{settings.ADMIN_PATH}",
            app=_get_wsgi_app(settings=settings),
            name="django-admin",
        ),
        ApplicationMount(
            path=f"{settings.STATIC_URL}",
            app=StaticFiles(directory=settings.STATIC_ROOT),
            name="django-static",
        ),
    ]
