from typing import TYPE_CHECKING, Callable, Literal, Protocol, Sequence

from fastapi import FastAPI
from starlette.datastructures import State

if TYPE_CHECKING:
    from django.conf import LazySettings
    from fastapi.middleware.wsgi import WSGIMiddleware
    from fastapi.staticfiles import StaticFiles

    from src.app.ports.outbound.db import DBPort

type EnvChoices = Literal["development", "testing", "staging", "production"]

type GetMountedApps = Callable[["LazySettings"], Sequence["_ApplicationMountProtocol"]]


class _ApplicationMountProtocol(Protocol):
    path: str
    app: "FastAPI | WSGIMiddleware | StaticFiles"
    name: str


class _CustomAppState(State):
    mounted_applications: list[_ApplicationMountProtocol]
    db: "DBPort"


class ASGIApp(FastAPI):
    state: _CustomAppState  # type: ignore
