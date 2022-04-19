from typing import Optional

from pydantic import BaseModel


class ModelProductForm(BaseModel):
    id: int
    new_name: str
    new_price: float

class ModelSizeForm(BaseModel):
    id: Optional[int] = None
    size: float
    length: Optional[float]
    price_for_sale: float


class ModelColorForm(BaseModel):
    name: str
    color: str
    new_color: str = None
    price_for_sale: float = None


class ModelShoesForm(BaseModel):
    name: str
    new_name: str = None
    price_for_sale: float = None
