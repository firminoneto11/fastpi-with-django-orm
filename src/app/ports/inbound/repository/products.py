from typing import Any, Optional

from src.domain.models import Product


class ProductRepoPort:
    async def list_(
        self, criteria: Optional[dict[str, Any]] = None
    ) -> list[Product]: ...

    async def retrieve(self, id_: str) -> Product | None: ...

    async def create(self, data: dict[str, Any]) -> Product: ...

    async def update(self, id_: str, data: dict[str, Any]) -> bool: ...

    async def delete(self, id_: str) -> bool: ...
