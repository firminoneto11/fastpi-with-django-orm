from fastapi import APIRouter

from .controllers import ProductsController

router = APIRouter(prefix="/v1", tags=["Core"])

router.add_api_route(
    path="/products",
    endpoint=ProductsController.get,
    methods=["GET"],
    status_code=200,
)

router.add_api_route(
    path="/products",
    endpoint=ProductsController.post,
    methods=["POST"],
    status_code=201,
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.get,
    methods=["GET"],
    status_code=200,
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.put,
    methods=["PUT"],
    status_code=200,
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.delete,
    methods=["DELETE"],
    status_code=204,
)
