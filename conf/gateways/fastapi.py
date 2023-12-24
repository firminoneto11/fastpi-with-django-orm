from os import environ

from django import setup
from fastapi import FastAPI


def get_fastapi_application():
    from django.conf import settings

    from conf.urls import routers

    application = FastAPI(debug=settings.DEBUG, title=settings.FASTAPI_TITLE)

    # Place middleware here

    [application.include_router(router=router, prefix="/api") for router in routers]

    return application


environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")


setup(set_prefix=False)
application = get_fastapi_application()
