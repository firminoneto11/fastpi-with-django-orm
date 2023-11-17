from typing import TYPE_CHECKING

from pytest import mark

from apps.core.models import Product
from apps.core.schemas import Product as ProductSchema

if TYPE_CHECKING:
    from httpx import AsyncClient


pytestmark = [mark.django_db(transaction=True)]


@mark.integration
async def test_list_products_should_list_registered_products(client: "AsyncClient"):
    """
    Test if the endpoint returns a list of registered products
    """

    products = [
        ProductSchema.model_validate(
            await Product.objects.acreate(name=name)
        ).model_dump(mode="json")
        for name in ("Product 1", "Product 2", "Product 3")
    ]

    response = await client.get("api/v1/products")

    assert response.status_code == 200
    assert response.json() == {"details": products}


@mark.integration
async def test_list_products_should_return_empty(client: "AsyncClient"):
    """
    Test if the endpoint returns an empty list when there are no registered products
    """

    response = await client.get("api/v1/products")

    assert response.status_code == 200
    assert response.json() == {"details": []}


@mark.integration
async def test_create_products(client: "AsyncClient"):
    """
    Test if the endpoint creates a new product
    """

    payload = {"name": "Product 1"}
    products_before = await Product.objects.acount()

    response = await client.post("api/v1/products", json=payload)

    products_after = await Product.objects.acount()
    product_created = await Product.objects.afirst()
    result_schema = ProductSchema.model_validate(product_created).model_dump(
        mode="json"
    )

    assert not products_before
    assert products_after == products_before + 1
    assert response.status_code == 201
    assert product_created.name == payload["name"]
    assert response.json() == result_schema
