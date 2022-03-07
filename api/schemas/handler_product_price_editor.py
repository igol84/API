from typing import Optional

from pydantic import BaseModel


class ModelProduct(BaseModel):
    id: Optional[int] = None
    size: float = None
    price_for_sale: float
