from fastapi import APIRouter

from .controllers import ProductsController

app_name, resource_name = "core", "products"
router = APIRouter(prefix="/v1", tags=["Core"])

router.add_api_route(
    path="/products",
    endpoint=ProductsController.get,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:{resource_name}:list",
)

router.add_api_route(
    path="/products",
    endpoint=ProductsController.post,
    methods=["POST"],
    status_code=201,
    name=f"{app_name}:{resource_name}:create",
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.get_one,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:{resource_name}:retrieve",
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.put,
    methods=["PUT"],
    status_code=200,
    name=f"{app_name}:{resource_name}:update",
)

router.add_api_route(
    path="/products/{product_id}",
    endpoint=ProductsController.delete,
    methods=["DELETE"],
    status_code=204,
    name=f"{app_name}:{resource_name}:delete",
)
