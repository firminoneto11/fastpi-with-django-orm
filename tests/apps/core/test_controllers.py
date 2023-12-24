from datetime import datetime
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


@mark.integration
async def test_get_product_by_id_should_raise_404_when_product_is_not_found(
    client: "AsyncClient",
):
    """
    Test if the endpoint raises a 404 when the product is not found
    """

    response = await client.get("api/v1/products/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product of id '1' not found"}


@mark.integration
async def test_get_product_by_id_should_return_the_product(client: "AsyncClient"):
    """
    Test if the endpoint returns the product
    """

    product = await Product.objects.acreate(name="Product 1")
    product = ProductSchema.model_validate(product).model_dump(mode="json")

    response = await client.get(f"api/v1/products/{product['id']}")

    assert response.status_code == 200
    assert response.json() == product


@mark.integration
async def test_update_product_should_raise_404_when_product_is_not_found(
    client: "AsyncClient",
):
    """
    Test if the endpoint raises a 404 when the product is not found
    """

    response = await client.put("api/v1/products/1", json={"name": "Product 1"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Product of id '1' not found"}


@mark.integration
async def test_update_product_should_update_the_product(client: "AsyncClient"):
    """
    Test if the endpoint updates the product
    """

    product = await Product.objects.acreate(name="Product 1")

    response = await client.put(
        f"api/v1/products/{product.id}", json={"name": "Product 2"}
    )

    product_updated = await Product.objects.afirst()
    result_schema = ProductSchema.model_validate(product_updated).model_dump(
        mode="json"
    )

    assert response.status_code == 200
    assert response.json() == result_schema
    assert product_updated.name == "Product 2"


@mark.integration
async def test_delete_product_should_raise_404_when_product_is_not_found(
    client: "AsyncClient",
):
    """
    Test if the endpoint raises a 404 when the product is not found
    """

    response = await client.delete("api/v1/products/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product of id '1' not found"}


@mark.integration
async def test_delete_product_should_delete_the_product(client: "AsyncClient"):
    """
    Test if the endpoint deletes the product
    """

    product = await Product.objects.acreate(name="Product 1")

    response = await client.delete(f"api/v1/products/{product.id}")

    qs = Product.objects.with_deleted()
    in_database = await Product.objects.fetch_qs(qs=qs)

    assert response.status_code == 204
    assert not await Product.objects.acount()
    assert len(in_database) == 1
    assert in_database[0].deleted
    assert isinstance(in_database[0].deleted_at, datetime)
