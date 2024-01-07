from os import environ

from django.core.asgi import get_asgi_application
from fastapi import FastAPI


def _setup_django_settings():
    environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    get_asgi_application()  # NOTE: We only call this so Django sets up the apps


def get_fastapi_application():
    from django.conf import settings

    from conf.urls import fastapi_routers as routers

    application = FastAPI(debug=settings.DEBUG, title=settings.FASTAPI_TITLE)

    # Place middleware here

    [application.include_router(router=router, prefix="/api") for router in routers]

    return application


_setup_django_settings()

application = get_fastapi_application()
