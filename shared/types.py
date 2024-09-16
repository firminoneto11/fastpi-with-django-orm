from typing import TYPE_CHECKING, Literal, Protocol

from fastapi import FastAPI
from starlette.datastructures import State

type EnvChoices = Literal["development", "testing", "staging", "production"]


if TYPE_CHECKING:
    # from src.application.ports.outbound.db import SqlDBPort
    ...


class _ApplicationMountProtocol(Protocol):
    path: str
    app: FastAPI
    name: str


class _CustomAppState(State):
    mounted_applications: list[_ApplicationMountProtocol]
    # db: "SqlDBPort"


class ASGIApp(FastAPI):
    state: _CustomAppState  # type: ignore
