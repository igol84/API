import datetime

from pydantic import BaseModel


class ItemFormEdit(BaseModel):
    id: int
    new_qty: int
    new_price: float


class SaleDetail(BaseModel):
    sale_id: int
    date: datetime.date
    qty: int
    price: float
