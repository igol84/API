from .. import tables
from ..schemas import sale as schemas_sale
from .base import CRUDBase


class Sale(CRUDBase[tables.Sale, schemas_sale.CreateSale, schemas_sale.BaseSale]):
    table = tables.Sale

    def create(self, request: schemas_sale.CreateSale) -> tables.Seller:
        sale_row = tables.Sale(**request.dict(exclude={'sale_line_items'}))
        sale_row.sale_line_items = [tables.SaleLineItem(**pd_sli.dict()) for pd_sli in request.sale_line_items]
        self.db.add(sale_row)
        self.db.commit()
        self.db.refresh(sale_row)
        return sale_row
