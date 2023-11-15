from typing import TYPE_CHECKING

from pytest import mark

from apps.core.models import Product
from apps.core.schemas import Product as ProductSchema

if TYPE_CHECKING:
    from httpx import AsyncClient


pytestmark = [mark.django_db(transaction=True)]


@mark.e2e
async def test_list_products_should_list_registered_products(client: "AsyncClient"):
    """
    Test if the endpoint returns a list of registered products
    """

    products = [
        ProductSchema.model_validate(await Product.objects.acreate(name=name))
        for name in ("Product 1", "Product 2", "Product 3")
    ]
    products = [product.model_dump(mode="json") for product in products]

    response = await client.get("api/v1/products")

    assert response.status_code == 200
    assert response.json() == {"details": products}


@mark.e2e
async def test_list_products_should_return_empty(client: "AsyncClient"):
    """
    Test if the endpoint returns an empty list when there are no registered products
    """

    response = await client.get("api/v1/products")

    assert response.status_code == 200
    assert response.json() == {"details": []}
