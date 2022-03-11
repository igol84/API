from typing import Optional

from pydantic import BaseModel


class ModelSize(BaseModel):
    id: Optional[int] = None
    size: float
    price_for_sale: float


class ModelColor(BaseModel):
    name: str
    color: str
    new_color: str = None
    price_for_sale: float = None


class ModelShoes(BaseModel):
    name: str
    new_name: str = None
    price_for_sale: float = None
