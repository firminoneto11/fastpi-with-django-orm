from fastapi import APIRouter, status

from src.app.services.product import ProductService
from src.domain.schemas.products import (
    CreateAndUpdateProductSchema,
    ProductSchemaOutput,
)
from src.infra.repository import ProductRepoAdapter

resource_name = "products"
router = APIRouter()


@router.get(
    "/products",
    name=f"{resource_name}:list",
    status_code=status.HTTP_200_OK,
    summary="Lists the products from the database",
    response_model=list[ProductSchemaOutput],
)
async def list_():
    repo = ProductRepoAdapter()
    svc = ProductService(repo=repo)
    return await svc.list_()


@router.post(
    "/products",
    name=f"{resource_name}:create",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new product",
    response_model=ProductSchemaOutput,
)
async def create(data: CreateAndUpdateProductSchema):
    repo = ProductRepoAdapter()
    svc = ProductService(repo=repo)
    return await svc.create(data=data)


@router.get(
    "/products/{id}",
    name=f"{resource_name}:retrieve",
    status_code=status.HTTP_200_OK,
    summary="Retrieves a single product from the database",
    response_model=ProductSchemaOutput,
)
async def retrieve(id: str):
    repo = ProductRepoAdapter()
    svc = ProductService(repo=repo)
    return await svc.retrieve(id_=id)


@router.put(
    "/products/{id}",
    name=f"{resource_name}:update",
    status_code=status.HTTP_200_OK,
    summary="Updates a product",
    response_model=ProductSchemaOutput,
)
async def update(id: str, data: CreateAndUpdateProductSchema):
    repo = ProductRepoAdapter()
    svc = ProductService(repo=repo)
    return await svc.update(id_=id, data=data)


@router.delete(
    "/products/{id}",
    name=f"{resource_name}:delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes a product from the database",
)
async def delete(id: str):
    repo = ProductRepoAdapter()
    svc = ProductService(repo=repo)
    return await svc.delete(id_=id)
