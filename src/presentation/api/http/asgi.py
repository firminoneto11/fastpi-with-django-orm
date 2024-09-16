from contextlib import asynccontextmanager
from os import environ
from typing import cast

from django import setup as setup_django
from fastapi import FastAPI

from shared.types import ASGIApp

from .routers import get_mounts


@asynccontextmanager
async def lifespan(app: ASGIApp):
    # await app.state.db.connect()
    yield
    # await app.state.db.disconnect()


class ASGIFactory:
    _apps_stack: list[ASGIApp] = []

    @classmethod
    def new(cls):
        cls._setup_django()
        application = cls().application
        cls._apps_stack.append(application)

        return application

    @classmethod
    def latest_app(cls):
        return cls._apps_stack[-1]

    @classmethod
    def _setup_django(cls):
        environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
        setup_django(set_prefix=False)

    def __init__(self):
        from django.conf import settings  # noqa

        self.application = cast(
            ASGIApp,
            # FastAPI(**settings.get_asgi_settings(main_mount=True), lifespan=lifespan),  # type: ignore # noqa
            FastAPI(lifespan=lifespan),  # type: ignore
        )

        self.setup_state()
        self.register_middleware()

    def setup_state(self):
        self.application.state.mounted_applications = []

        for mount in get_mounts():
            self.application.mount(path=mount.path, app=mount.app, name=mount.name)
            self.application.state.mounted_applications.append(mount)

    def register_middleware(self):
        from .middleware import (
            allowed_hosts_middleware_configuration,
            cors_middleware_configuration,
        )

        self.application.add_middleware(**allowed_hosts_middleware_configuration)  # type: ignore
        self.application.add_middleware(**cors_middleware_configuration)  # type: ignore


app = ASGIFactory.new()
