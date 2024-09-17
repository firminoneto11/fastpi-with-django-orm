from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from src.domain.models import Product


class ProductRepoPort:
    async def list_(
        self, criteria: Optional[dict[str, Any]] = None
    ) -> list["Product"]: ...

    async def retrieve(self, /, **criteria: Any) -> "Product | None": ...

    async def create(self, data: dict[str, Any]) -> "Product": ...

    async def update(self, id_: str, data: dict[str, Any]) -> "Product | None": ...

    async def delete(self, id_: str) -> bool: ...
