from .core.urls import router as core_router


def collect_routers():
    return [core_router]
