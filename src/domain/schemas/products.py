from datetime import datetime
from decimal import Decimal

from .base import CamelModel


class CreateAndUpdateProductSchema(CamelModel):
    name: str
    price: Decimal


class ProductSchemaOutput(CamelModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    price: Decimal
