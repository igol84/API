from pydantic import BaseModel
from datetime import datetime

class BaseSale(BaseModel):
    store_id: int
    seller_id: int
    place_id: int
    date_time: datetime


class CreateSale(BaseSale):
    pass


class Sale(BaseSale):
    id: int


    class Config:
        orm_mode = True

class ShowSaleWithProduct(Sale):
    pass