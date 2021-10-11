from .. import tables
from ..schemas import sale_line_item as schemas
from .base import CRUDBase


class SaleLineItem(CRUDBase[tables.SaleLineItem, schemas.CreateSaleLineItem, schemas.UpdateSaleLineItem]):
    table = tables.SaleLineItem
    schema = schemas.BaseSaleLineItem
    keys = ['sale_id', 'item_id', 'sale_price']
    autoincrement = False
