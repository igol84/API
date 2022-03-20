from enum import Enum
from typing import Optional
from pydantic import BaseModel

from api.schemas.item import Item
from api.schemas.product import Product


class ModelSizeShoes(BaseModel):
    size: Optional[float] = None
    length: Optional[float] = None
    qty: Optional[int] = None


class ModelShoes(BaseModel):
    width: Optional[str] = None
    color: Optional[str] = None
    sizes: list[ModelSizeShoes]


class Type(Enum):
    product = 'product'
    shoes = 'shoes'


class ModelProduct(BaseModel):
    id: Optional[int] = None
    store_id: int
    type: Type = Type.product
    name: str
    price_sell: float
    price_buy: Optional[float] = None
    qty: Optional[int] = None
    module: Optional[ModelShoes] = None


class OutputItems(BaseModel):
    products: Optional[list[Product]] = None
    items: list[Item]
