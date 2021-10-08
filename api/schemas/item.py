from pydantic import BaseModel
from .product import Product


class BaseItem(BaseModel):
    prod_id: int
    store_id: int
    qty: int
    buy_price: float


class CreateItem(BaseItem):
    pass


class Item(BaseItem):
    id: int

    class Config:
        orm_mode = True


class ShowItemWithProduct(Item):
    product: Product
