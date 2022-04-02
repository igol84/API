from pydantic import BaseModel


class ItemFormEdit(BaseModel):
    id: int
    new_qty: int
    new_price: float


class ItemFormDel(BaseModel):
    id: int
