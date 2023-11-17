"""
ASGI config for conf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI


def get_fastapi_application():
    from django.conf import settings

    from .urls import routers

    application_ = FastAPI(debug=settings.DEBUG, title=settings.FASTAPI_TITLE)

    # Place middleware here

    [application_.include_router(router=router, prefix="/api") for router in routers]

    return application_


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

application = get_asgi_application()
app = get_fastapi_application()
