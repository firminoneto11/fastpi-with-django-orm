from typing import Optional

from .schemas import ProductInputSchema, ProductSchema
from .services import ProductService


class ProductsController:
    @staticmethod
    async def get(
        product_id: Optional[str] = None
    ) -> dict[str, list[ProductSchema]] | ProductSchema:
        svc = ProductService()
        if product_id:
            return await svc.get_product_by_id(product_id=product_id)
        return await svc.list_products()

    @staticmethod
    async def post(data: ProductInputSchema) -> ProductSchema:
        svc = ProductService()
        return await svc.create_product(data)

    @staticmethod
    async def put(product_id: str, data: ProductInputSchema) -> ProductSchema:
        svc = ProductService()
        return await svc.update_product(product_id=product_id, data=data)

    @staticmethod
    async def delete(product_id: str) -> None:
        svc = ProductService()
        return await svc.delete(product_id=product_id)
