from fastapi import HTTPException

from .models import Product
from .schemas import Product as ProductSchema
from .schemas import ProductInput


async def list_products() -> dict[str, list[ProductSchema]]:
    return {"details": await Product.fetch_all()}


async def create_product(data: ProductInput) -> ProductSchema:
    return await Product.objects.acreate(name=data.name)


async def get_product_by_id(product_id: str) -> ProductSchema:
    try:
        product = await Product.objects.aget(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"Product of id {product_id!r} not found"
        )
    return product


async def update_product(product_id: str, data: ProductInput) -> ProductSchema:
    try:
        product = await Product.objects.aget(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"Product of id {product_id!r} not found"
        )
    product.name = data.name
    await product.asave()
    return product


async def delete_product(product_id: str) -> None:
    try:
        product = await Product.objects.aget(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"Product of id {product_id!r} not found"
        )
    await product.adelete()
