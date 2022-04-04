from fastapi import Depends, status
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas import handler_items_editor as schemas


class HandlerItemEditor:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_item(self, data: schemas.ItemFormEdit) -> schemas.ItemFormEdit:
        item = self.db.query(tables.Item).filter(tables.Item.id == data.id)
        item_row = item.first()
        edited = False
        if item_row.buy_price != data.new_price:
            edited = True
            item.update({'buy_price': data.new_price})
        if item_row.qty != data.new_qty:
            edited = True
            item.update({'qty': data.new_qty})
        item_row = item.first()
        if edited:
            self.db.commit()
        return schemas.ItemFormEdit(id=item_row.id, new_price=item_row.buy_price, new_qty=item_row.qty)

    def del_item(self, item_id: int) -> None:
        item = self.db.query(tables.Item).filter(tables.Item.id == item_id)
        if not item.first():
            key_m = f'item_id:{item_id}'
            err_mess = f'Item with the {key_m} not available'
            from fastapi import HTTPException
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
        item.delete(synchronize_session=False)
        self.db.commit()

    def get_item_sales(self, item_id: int) -> list[schemas.SaleDetail]:
        sales = self.db.query(tables.Sale, tables.SaleLineItem).filter(
            tables.SaleLineItem.item_id == item_id,
            tables.Sale.id == tables.SaleLineItem.sale_id
        ).all()
        db_sizes = []
        for sale, sli in sales:
            date = sale.date_time.date()
            db_sizes.append(schemas.SaleDetail(sale_id=sale.id, date=date, qty=sli.qty, price=sli.sale_price))
        return db_sizes
