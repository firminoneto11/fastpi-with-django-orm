from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from src.domain.models import Product


class ProductRepoPort(metaclass=ABCMeta):
    @abstractmethod
    async def list_(
        self, criteria: Optional[dict[str, Any]] = None
    ) -> list["Product"]: ...

    @abstractmethod
    async def retrieve(self, /, **criteria: Any) -> "Product | None": ...

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> "Product": ...

    @abstractmethod
    async def update(self, id_: str, data: dict[str, Any]) -> "Product | None": ...

    @abstractmethod
    async def delete(self, id_: str) -> bool: ...
