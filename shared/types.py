from typing import TYPE_CHECKING, Literal, Protocol

from fastapi import FastAPI
from starlette.datastructures import State

type EnvChoices = Literal["development", "testing", "staging", "production"]


if TYPE_CHECKING:
    # from src.application.ports.outbound.db import SqlDBPort
    from fastapi.middleware.wsgi import WSGIMiddleware
    from fastapi.staticfiles import StaticFiles


class _ApplicationMountProtocol(Protocol):
    path: str
    app: "FastAPI | WSGIMiddleware | StaticFiles"
    name: str


class _CustomAppState(State):
    mounted_applications: list[_ApplicationMountProtocol]
    # db: "SqlDBPort"


class ASGIApp(FastAPI):
    state: _CustomAppState  # type: ignore
