from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductInputSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
