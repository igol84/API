from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.header_sale_registration import EditSLIPrice, PutItemToOldSale


class HeaderSaleRegistration:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_sli_price(self, request: EditSLIPrice) -> None:
        old_sli = request.old_sli
        table = tables.SaleLineItem
        old_row_sli = self.db.query(tables.SaleLineItem).filter(
            table.sale_id == old_sli.sale_id,
            table.item_id == old_sli.item_id,
            table.sale_price == old_sli.sale_price
        )
        if not old_row_sli.first():
            key_m = f'sale_id:{old_sli.sale_id}, item_id:{old_sli.item_id}, sale_price:{old_sli.sale_price}'
            err_mess = f'{table.__name__} with the {key_m} not available'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
        old_row_sli.delete(synchronize_session=False)
        new_sli_row = table(**request.new_sli.dict())
        self.db.add(new_sli_row)
        self.db.commit()

    def put_items_from_old_sale(self, request: PutItemToOldSale) -> None:
        table = tables.SaleLineItem
        for del_sli in request.list_del_sli:
            row_sli = self.db.query(table).filter(
                table.sale_id == del_sli.sale_id,
                table.item_id == del_sli.item_id,
                table.sale_price == del_sli.sale_price
            )
            if not row_sli.first():
                key_m = f'sale_id:{del_sli.sale_id}, item_id:{del_sli.item_id}, sale_price:{del_sli.sale_price}'
                err_mess = f'{table.__name__} with the {key_m} not available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
            row_sli.delete(synchronize_session=False)

        table = tables.Item
        for pd_item in request.list_new_items:
            new_item = table(**pd_item.dict())
            self.db.add(new_item)

        for pd_item in request.list_update_items:
            row_item = self.db.query(table).filter(table.id == pd_item.id)
            if not row_item.first():
                key_m = f'item_id:{pd_item.id}'
                err_mess = f'{table.__name__} with the {key_m} not available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
            row_item.update(pd_item.dict())

        if request.delete:
            table = tables.Sale
            row_sale = self.db.query(table).filter(table.id == request.sale_id)
            if not row_sale.first():
                key_m = f'sale_id:{request.sale_id}'
                err_mess = f'{table.__name__} with the {key_m} not available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
            row_sale.delete(synchronize_session=False)
        self.db.commit()
