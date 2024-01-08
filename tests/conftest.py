from httpx import AsyncClient
from pytest import fixture, mark, param

pytestmark = [mark.anyio]


@fixture(params=[param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop")])
def anyio_backend(request):
    return request.param


@fixture(scope="session")
def app():
    """Returns a FastAPI app instance"""

    from conf.gateways.fastapi import application

    return application


@fixture
async def client(app):
    """Returns a TestClient instance"""

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
