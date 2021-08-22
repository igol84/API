from typing import Optional

from pydantic import BaseModel

from .shoes import Shoes


class BaseProduct(BaseModel):
    type: str
    name: str
    price: float


class CreateProduct(BaseProduct):
    pass


class Product(BaseProduct):
    id: int
    shoes: Optional[Shoes] = None

    class Config:
        orm_mode = True
