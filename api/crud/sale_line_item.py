from .. import tables
from ..schemas import sale_line_item as schemas
from .base import CRUDBase, HTTPException, status


class SaleLineItem(CRUDBase[tables.SaleLineItem, schemas.CreateSaleLineItem, schemas.BaseSaleLineItem]):
    table = tables.SaleLineItem
    schema = schemas.BaseSaleLineItem

    def _get_sli(self, sale_id: int, item_id: int, sale_price: float):
        db_obj = self.db.query(self.table).filter(
            self.table.sale_id == sale_id,
            self.table.item_id == item_id,
            self.table.sale_price == sale_price
        )
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} with the sale_id \'{sale_id}\''
                                       f' and item_id \'{item_id}\' and sale_price \'{sale_price}\' is not available')
        return db_obj

    def get_sli(self, sale_id: int, item_id: int, sale_price: float) -> table:
        return self._get_sli(sale_id, item_id, sale_price).first()

    def update_sli(self, sale_id: int, item_id: int, sale_price: float, request: schema) -> table:
        db_obj = self._get_sli(sale_id, item_id, sale_price)
        db_obj.update(request.dict())
        self.db.commit()
        return db_obj.first()

    def delete_sli(self, sale_id: int, item_id: int, sale_price: float):
        db_obj = self._get_sli(sale_id, item_id, sale_price)
        db_obj.delete(synchronize_session=False)
        self.db.commit()
