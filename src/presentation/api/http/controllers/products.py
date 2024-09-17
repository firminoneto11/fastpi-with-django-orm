from fastapi import APIRouter

from src.app.services.product import ProductService
from src.infra.repository import ProductRepoAdapter

resource_name = "products"
router = APIRouter()


@router.get("/products", name=f"{resource_name}:list")
async def list_():
    svc = ProductService(repo=ProductRepoAdapter())
    return await svc.list_()


@router.post("/products", name=f"{resource_name}:create")
async def create():
    svc = ProductService(repo=ProductRepoAdapter())
    return await svc.create()


@router.get("/products/{id_}", name=f"{resource_name}:retrieve")
async def retrieve(id_: str):
    svc = ProductService(repo=ProductRepoAdapter())
    return await svc.retrieve(id_=id_)


@router.put("/products/{id_}", name=f"{resource_name}:update")
async def update(id_: str):
    svc = ProductService(repo=ProductRepoAdapter())
    return await svc.update(id_=id_)


@router.delete("/products/{id_}", name=f"{resource_name}:delete")
async def delete(id_: str):
    svc = ProductService(repo=ProductRepoAdapter())
    return await svc.delete(id_=id_)
