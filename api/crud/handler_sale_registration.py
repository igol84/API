from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.handler_sale_registration import EditSLIPrice, PutItemToOldSale, EndSale, OutputEndSale
from ..schemas.item import Item
from ..schemas.sale import ShowSaleWithSLIs


class HeaderSaleRegistration:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def end_sale(self, data: EndSale) -> OutputEndSale:
        pd_sale = data.sale
        sale_row = tables.Sale(**pd_sale.dict(exclude={'sale_line_items'}))
        sale_row.sale_line_items = [tables.SaleLineItem(**pd_sli.dict()) for pd_sli in pd_sale.sale_line_items]
        self.db.add(sale_row)

        # Update qty in items
        for pd_sli in pd_sale.sale_line_items:
            item_row = self.db.query(tables.Item).filter(tables.Item.id == pd_sli.item_id)
            item_pd = Item.from_orm(item_row.first())
            item_pd.qty -= pd_sli.qty
            item_row.update(item_pd.dict())

        self.db.commit()
        self.db.refresh(sale_row)
        pd_new_sale = ShowSaleWithSLIs.from_orm(sale_row)
        pd_output = OutputEndSale(sale=pd_new_sale)
        return pd_output

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
        # delete sale items
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
        # create items
        table = tables.Item
        for pd_item in request.list_new_items:
            new_item = table(**pd_item.dict())
            self.db.add(new_item)
        # update items
        for pd_item in request.list_update_items:
            row_item = self.db.query(table).filter(table.id == pd_item.id)
            if not row_item.first():
                key_m = f'item_id:{pd_item.id}'
                err_mess = f'{table.__name__} with the {key_m} not available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
            row_item.update(pd_item.dict())
        # delete empty sale
        if request.delete:
            table = tables.Sale
            row_sale = self.db.query(table).filter(table.id == request.sale_id)
            if not row_sale.first():
                key_m = f'sale_id:{request.sale_id}'
                err_mess = f'{table.__name__} with the {key_m} not available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mess)
            row_sale.delete(synchronize_session=False)
        self.db.commit()
