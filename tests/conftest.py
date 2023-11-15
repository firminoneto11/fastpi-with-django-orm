from asyncio import new_event_loop, set_event_loop

from httpx import AsyncClient
from pytest import fixture
from uvloop import install as install_uvloop


@fixture(scope="session", autouse=True)
def event_loop():
    """Overrides pytest's default function scoped event loop"""

    install_uvloop()
    loop = new_event_loop()
    set_event_loop(loop=loop)

    yield loop

    if loop.is_running():
        loop.stop()

    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.run_until_complete(loop.shutdown_default_executor())
    loop.close()


@fixture(scope="session")
def app():
    """Returns a FastAPI app instance"""

    from conf.asgi import app

    return app


@fixture
async def client(app):
    """Returns a TestClient instance"""

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
