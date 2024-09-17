from dataclasses import dataclass

from src.app.exceptions import ObjectNotFound
from src.app.ports.inbound.repository import ProductRepoPort
from src.domain.schemas.products import CreateAndUpdateProductSchema


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
        # TODO: What is the best way to do validations? Bring in django rest framework?
        return await self.repo.create(data=data.model_dump())

    async def update(self, id_: str, data: CreateAndUpdateProductSchema):
        if product := await self.repo.update(id_=id_, data=data.model_dump()):
            return product

        raise ObjectNotFound(f"Product of id {id_!r} not found")

    async def delete(self, id_: str):
        deleted = await self.repo.delete(id_=id_)
        if not deleted:
            raise ObjectNotFound(f"Product of id {id_!r} not found")
