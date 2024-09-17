from contextlib import asynccontextmanager
from os import environ
from typing import TYPE_CHECKING, cast

from django import setup
from fastapi import FastAPI

from shared.types import ASGIApp
from src.infra.db import DBAdapter
from src.presentation.api.http.middleware import (
    get_allowed_hosts_config,
    get_cors_config,
)

if TYPE_CHECKING:
    from django.conf import LazySettings


@asynccontextmanager
async def lifespan(app: ASGIApp):
    await app.state.db.ping(raise_exc=True)
    yield


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
        setup(set_prefix=False)

    def __init__(self):
        from django.conf import settings

        self.application = cast(
            ASGIApp,
            FastAPI(**settings.GET_ASGI_SETTINGS(main_mount=True), lifespan=lifespan),  # type: ignore
        )

        self.setup_state(settings=settings)
        self.register_middleware(settings=settings)

    def setup_state(self, settings: "LazySettings"):
        from .routers import get_mounts

        self.application.state.db = DBAdapter()
        self.application.state.mounted_applications = []

        for mount in get_mounts(settings=settings):
            self.application.mount(path=mount.path, app=mount.app, name=mount.name)
            self.application.state.mounted_applications.append(mount)

    def register_middleware(self, settings: "LazySettings"):
        self.application.add_middleware(**get_allowed_hosts_config(settings=settings))  # type: ignore
        self.application.add_middleware(**get_cors_config(settings=settings))  # type: ignore


app = ASGIFactory.new()
