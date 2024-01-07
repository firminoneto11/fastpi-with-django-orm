from typing import TYPE_CHECKING

from shared.utils import get_object_or_404

from .models import Product

if TYPE_CHECKING:
    from .schemas import ProductInputSchema


class ProductService:
    async def list_products(self):
        return await Product.objects.fetch_qs(qs=Product.objects.all())

    async def create_product(self, data: "ProductInputSchema"):
        return await Product.objects.acreate(name=data.name)

    async def get_product_by_id(self, product_id: str):
        return await get_object_or_404(
            Product, f"Product of id {product_id!r} not found", product_id=product_id
        )

    async def update_product(self, product_id: str, data: "ProductInputSchema"):
        product = await self.get_product_by_id(product_id=product_id)
        return await product.update(data=data)

    async def delete_product(self, product_id: str):
        product = await self.get_product_by_id(product_id=product_id)
        await product.adelete()
