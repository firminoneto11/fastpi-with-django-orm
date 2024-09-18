from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from .base import CamelModel


class CreateProductSchema(CamelModel):
    name: str
    price: Decimal


class UpdateProductSchema(CamelModel):
    name: Optional[str] = Field(default=None)
    price: Optional[str] = Field(default=None)


class OutputProductSchema(CamelModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    price: Decimal
