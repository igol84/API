from pydantic import BaseModel

from .item import CreateItem, UpdateItem
from .sale_line_item import SaleLineItem


class EditSLIPrice(BaseModel):
    old_sli: SaleLineItem
    new_sli: SaleLineItem

class SaleLineItemKeys(BaseModel):
    sale_id: int
    item_id: int
    sale_price: float

class PutItemToOldSale(BaseModel):
    sale_id: int
    list_del_sli: list[SaleLineItemKeys]
    list_new_items: list[CreateItem]
    list_update_items: list[UpdateItem]
    delete: bool = False
