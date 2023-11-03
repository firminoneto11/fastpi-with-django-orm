from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductInput(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
