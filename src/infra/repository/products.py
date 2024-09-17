from typing import Any, Optional

from src.app.ports.inbound.repository import ProductRepoPort
from src.domain.models import Product


class ProductRepoAdapter(ProductRepoPort):
    async def list_(self, criteria: Optional[dict[str, Any]] = None):
        qs = Product.objects.all()

        if criteria:
            qs = qs.filter(**criteria)

        return [product async for product in qs]

    async def retrieve(self, id_: str):
        return await Product.objects.filter(id=id_).afirst()

    async def create(self, data: dict[str, Any]):
        return await Product.objects.acreate(**data)

    async def update(self, id_: str, data: dict[str, Any]):
        exists = False
        if product := await self.retrieve(id_=id_):
            await product.update(data=data)
            exists = True

        return exists

    async def delete(self, id_: str):
        exists = False
        if product := await self.retrieve(id_=id_):
            await product.adelete()
            exists = True

        return exists
