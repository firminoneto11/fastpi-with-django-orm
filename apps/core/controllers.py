from .schemas import ProductInputSchema, ProductSchema
from .services import ProductService


class ProductsController:
    @staticmethod
    async def get() -> list[ProductSchema]:
        svc = ProductService()
        return await svc.list_products()

    @staticmethod
    async def get_one(product_id: str) -> ProductSchema:
        svc = ProductService()
        return await svc.get_product_by_id(product_id=product_id)

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
        return await svc.delete_product(product_id=product_id)
