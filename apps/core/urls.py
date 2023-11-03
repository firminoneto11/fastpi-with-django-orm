from fastapi import APIRouter

from .controllers import (
    create_product,
    delete_product,
    get_product_by_id,
    list_products,
    update_product,
)

router = APIRouter(prefix="/v1", tags=["Core"])

router.add_api_route(path="/products", endpoint=list_products, methods=["GET"])

router.add_api_route(
    path="/products/{product_id}", endpoint=get_product_by_id, methods=["GET"]
)

router.add_api_route(
    path="/products",
    endpoint=create_product,
    methods=["POST"],
    status_code=201,
)

router.add_api_route(
    path="/products/{product_id}", endpoint=update_product, methods=["PUT"]
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=delete_product,
    methods=["DELETE"],
    status_code=204,
)
