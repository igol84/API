from pydantic import BaseModel
from datetime import datetime
from .sale_line_item import ShowSaleLineItemWithItem, CreateSaleLineItemForSale
from .seller import Seller
from .place import Place


class BaseSale(BaseModel):
    seller_id: int
    place_id: int
    date_time: datetime


class CreateSale(BaseSale):
    sale_line_items: list[CreateSaleLineItemForSale]


class UpdateSale(CreateSale):
    id: int


class Sale(UpdateSale):

    class Config:
        orm_mode = True


class ShowSaleWithSLIs(Sale):
    sale_line_items: list[ShowSaleLineItemWithItem]
    seller: Seller
    place: Place
