from dataclasses import dataclass

from fastapi import FastAPI

from .controllers import misc_router


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI
    name: str


def _get_app_v1():
    # TODO: Add the params
    app_v1 = FastAPI()

    app_v1.include_router(misc_router)

    return app_v1


def get_mounts():
    return [ApplicationMount(path="/api/v1", app=_get_app_v1(), name="v1")]
