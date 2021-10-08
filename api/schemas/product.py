from typing import Optional
from pydantic import BaseModel
from .shoes import CreateShoesWithProduct, Shoes


class BaseProduct(BaseModel):
    type: str
    name: str
    price: float


class CreateProduct(BaseProduct):
    shoes: Optional[CreateShoesWithProduct] = None


class UpdateProduct(CreateProduct):
    id: Optional[int] = None


class Product(BaseProduct):
    id: int
    shoes: Optional[Shoes] = None

    class Config:
        orm_mode = True
