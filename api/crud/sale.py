from .. import tables
from ..schemas import sale as schemas_sale
from .base import CRUDBase


class Sale(CRUDBase[tables.Sale, schemas_sale.CreateSale, schemas_sale.BaseSale]):
    table = tables.Sale

    def create(self, request: schemas_sale.CreateSale) -> tables.Sale:
        sale_row = tables.Sale(**request.dict(exclude={'sale_line_items'}))
        sale_row.sale_line_items = [tables.SaleLineItem(**pd_sli.dict()) for pd_sli in request.sale_line_items]
        self.db.add(sale_row)
        self.db.commit()
        self.db.refresh(sale_row)
        return sale_row

    def update(self, request: schemas_sale.UpdateSale) -> tables.Sale:
        sale_row = self._get(request.id)
        sli_rows = self.db.query(tables.SaleLineItem).filter(tables.SaleLineItem.sale_id == request.id)
        sli_rows.delete(synchronize_session=False)
        sale_row.update(request.dict(exclude={'sale_line_items'}))
        sale_line_items = [tables.SaleLineItem(sale_id=request.id, **pd_sli.dict()) for pd_sli in request.sale_line_items]
        self.db.add_all(sale_line_items)
        self.db.commit()
        return sale_row.first()

    def delete(self, sale_id: int):
        sale_row = self._get(sale_id)
        sale_row.delete(synchronize_session=False)
        list_rows_sli = self.db.query(tables.SaleLineItem).filter(tables.SaleLineItem.sale_id == sale_id)
        list_rows_sli.delete(synchronize_session=False)
        self.db.commit()
