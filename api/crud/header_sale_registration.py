from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.header_sale_registration import EditSLIPrice


class HeaderSaleRegistration:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_sli_price(self, request: EditSLIPrice) -> list[tables.SaleLineItem]:
        old_sli = request.old_sli
        table = tables.SaleLineItem
        old_row_sli = self.db.query(tables.SaleLineItem).filter(
            table.sale_id == old_sli.sale_id,
            table.item_id == old_sli.item_id,
            table.sale_price == old_sli.sale_price
        )
        if not old_row_sli.first():
            key_m = f'sale_id:{old_sli.sale_id}, item_id:{old_sli.item_id}, sale_price:{old_sli.sale_price}'
            err_mes = f'{table.__name__} with the {key_m} not available'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mes)
        old_row_sli.delete(synchronize_session=False)
        new_sli_row = table(**request.new_sli.dict())
        self.db.add(new_sli_row)
        self.db.commit()
        self.db.refresh(new_sli_row)
        return new_sli_row
