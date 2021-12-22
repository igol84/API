from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.header_sale_registration import EditSLIPrice


class HeaderSaleRegistration:
    keys = ['sale_id', 'item_id', 'sale_price']
    autoincrement = False

    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def _get(self, table, *keys):
        dict_keys = dict(zip(self.keys, keys))
        filter_table = [getattr(table, key) == value for key, value in dict_keys.items()]
        db_obj = self.db.query(table).filter(*filter_table)
        if not db_obj.first():
            key_m = ', '.join([f'\'{key}\':\'{value}\'' for key, value in dict_keys.items()])
            err_mes = f'{table.__name__} with the {key_m} not available'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mes)
        return db_obj

    def edit_sli_price(self, request: EditSLIPrice) -> list[tables.SaleLineItem]:
        keys_old_sli = [getattr(request.old_sli, key) for key in self.keys]
        old_row_sli = self._get(tables.SaleLineItem, *keys_old_sli)
        old_row_sli.delete(synchronize_session=False)
        new_db_obj = tables.SaleLineItem(**request.new_sli.dict())
        self.db.add(new_db_obj)
        self.db.commit()
        self.db.refresh(new_db_obj)
        return new_db_obj
