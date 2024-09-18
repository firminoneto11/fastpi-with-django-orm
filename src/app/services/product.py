from dataclasses import dataclass

from src.app.exceptions import ObjectNotFound
from src.app.ports.inbound.repository import ProductRepoPort
from src.domain.schemas.products import CreateAndUpdateProductSchema
from src.domain.serializers import ProductSerializer


@dataclass
class ProductService:
    repo: ProductRepoPort

    async def list_(self):
        return await self.repo.list_()

    async def retrieve(self, id_: str):
        if product := await self.repo.retrieve(id=id_):
            return product

        raise ObjectNotFound(f"Product of id {id_!r} not found")

    async def create(self, data: CreateAndUpdateProductSchema):
        serializer = ProductSerializer(data=data.model_dump())

        await serializer.async_is_valid(raise_exception=True)

        validated_data = await serializer.adata  # type: ignore
        return await self.repo.create(data=validated_data)  # type: ignore

    async def update(self, id_: str, data: CreateAndUpdateProductSchema):
        if product := await self.repo.retrieve(id=id_):
            serializer = ProductSerializer(data=data.model_dump())

            await serializer.async_is_valid(raise_exception=True)

            validated_data = await serializer.adata  # type: ignore
            await serializer.aupdate(product, validated_data)  # type: ignore

            return product

        raise ObjectNotFound(f"Product of id {id_!r} not found")

    async def delete(self, id_: str):
        deleted = await self.repo.delete(id_=id_)
        if not deleted:
            raise ObjectNotFound(f"Product of id {id_!r} not found")
