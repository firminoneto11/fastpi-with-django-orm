from contextlib import asynccontextmanager
from os import environ
from typing import TYPE_CHECKING, cast

from django import setup
from fastapi import FastAPI
from rest_framework.exceptions import ValidationError

from shared.types import ASGIApp, GetMountedApps
from src.infra.db import DBAdapter

from .exception_handlers import drf_validation_error_handler
from .middleware import get_allowed_hosts_config, get_cors_config

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

        from .routers import get_mounted_apps

        self.application = cast(
            ASGIApp,
            FastAPI(**settings.GET_ASGI_SETTINGS(main_mount=True), lifespan=lifespan),  # type: ignore
        )

        self.setup_state(settings=settings, get_mounted_apps=get_mounted_apps)
        self.setup_middleware(settings=settings)
        self.setup_exception_handlers()

    def setup_state(self, settings: "LazySettings", get_mounted_apps: GetMountedApps):
        self.application.state.db = DBAdapter()
        self.application.state.mounted_applications = []

        for mount in get_mounted_apps(settings):
            self.application.mount(path=mount.path, app=mount.app, name=mount.name)
            self.application.state.mounted_applications.append(mount)

    def setup_middleware(self, settings: "LazySettings"):
        # TODO: Should we add the middleware for every sub app?
        self.application.add_middleware(**get_allowed_hosts_config(settings=settings))  # type: ignore
        self.application.add_middleware(**get_cors_config(settings=settings))  # type: ignore

    def setup_exception_handlers(self):
        pairs = [
            {
                "exc": ValidationError,
                "handler": drf_validation_error_handler,
            },
        ]

        for pair in pairs:
            for mount in self.application.state.mounted_applications:
                if isinstance(mount.app, FastAPI):
                    mount.app.add_exception_handler(pair["exc"], pair["handler"])  # type: ignore


app = ASGIFactory.new()
