from .base import CRUDBase
from .. import tables
from ..schemas import sale_line_item as schemas
from ..schemas.handler_sale_registration import EditSLIPrice


class SaleLineItem(CRUDBase[tables.SaleLineItem, schemas.CreateSaleLineItem, schemas.UpdateSaleLineItem]):
    table = tables.SaleLineItem
    keys = ['sale_id', 'item_id', 'sale_price']
    autoincrement = False

    def edit_sli_price(self, request: EditSLIPrice) -> list[tables.SaleLineItem]:
        keys_old_sli = [getattr(request.old_sli, key) for key in self.keys]
        old_row_sli = self._get(*keys_old_sli)
        old_row_sli.delete(synchronize_session=False)
        new_db_obj = tables.SaleLineItem(**request.new_sli.dict())
        self.db.add(new_db_obj)
        self.db.commit()
        self.db.refresh(new_db_obj)
        return new_db_obj
