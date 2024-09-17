from datetime import datetime
from decimal import Decimal

from pydantic import Field

from .base import CamelModel


class CreateAndUpdateProductSchema(CamelModel):
    name: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(max_digits=10, decimal_places=2)


class ProductSchemaOutput(CamelModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    price: Decimal
