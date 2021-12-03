import datetime
from collections import Counter

from .. import tables
from ..schemas import sale as schemas_sale
from ..schemas import item as schemas_item
from .base import CRUDBase


class Sale(CRUDBase[tables.Sale, schemas_sale.CreateSale, schemas_sale.BaseSale]):
    table = tables.Sale

    def get_all(self, skip: int = 0, limit: int = None, date: str = None, place_id: int = None,
                seller_id: int = None, store_id: int = None) -> list[table]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table)
        if store_id:
            db_obj = db_obj.from_self().join(tables.Place).filter(tables.Place.store_id == store_id)
        if date:
            date_dt_min = datetime.datetime.fromisoformat(date).date()
            date_dt_max = datetime.datetime.fromisoformat(date).date() + datetime.timedelta(days=1)
            db_obj = db_obj.filter(self.table.date_time >= date_dt_min).filter(self.table.date_time < date_dt_max)
        if place_id:
            db_obj = db_obj.filter(self.table.place_id == place_id)
        if seller_id:
            db_obj = db_obj.filter(self.table.seller_id == seller_id)

        return db_obj[SLICE]

    def create(self, request: schemas_sale.CreateSale) -> tables.Sale:
        sale_row = tables.Sale(**request.dict(exclude={'sale_line_items'}))
        sale_row.sale_line_items = [tables.SaleLineItem(**pd_sli.dict()) for pd_sli in request.sale_line_items]
        self.db.add(sale_row)

        # Update qty in items
        for pd_sli in request.sale_line_items:
            item_row = self.db.query(tables.Item).filter(tables.Item.id == pd_sli.item_id)
            item_pd = schemas_item.Item.from_orm(item_row.first())
            item_pd.qty -= pd_sli.qty
            item_row.update(item_pd.dict())

        self.db.commit()
        self.db.refresh(sale_row)
        return sale_row

    def update(self, request: schemas_sale.UpdateSale) -> tables.Sale:
        sale_row = self._get(request.id)
        sli_rows = self.db.query(tables.SaleLineItem).filter(tables.SaleLineItem.sale_id == request.id)

        # Update qty in items
        dict_sli_s = {sli.item_id: sli.qty for sli in sli_rows}
        dict_new_sli_s = {sli.item_id: sli.qty for sli in request.sale_line_items}
        count_sli_s, count_new_sli_s = Counter(), Counter()
        for item_id_, qty_ in dict_sli_s.items():
            count_sli_s[item_id_] += qty_
        for item_id_, qty_ in dict_new_sli_s.items():
            count_new_sli_s[item_id_] += qty_
        items_ids = list(dict_sli_s | dict_new_sli_s)
        need_update_items = [item_id_ for item_id_ in items_ids if count_sli_s[item_id_] != count_new_sli_s[item_id_]]
        for item_id_ in need_update_items:
            item_row = self.db.query(tables.Item).filter(tables.Item.id == item_id_)
            item_pd = schemas_item.Item.from_orm(item_row.first())
            item_pd.qty += count_sli_s[item_id_] - count_new_sli_s[item_id_]
            item_row.update(item_pd.dict())

        sli_rows.delete(synchronize_session=False)
        sale_row.update(request.dict(exclude={'sale_line_items'}))
        sale_line_items = [tables.SaleLineItem(sale_id=request.id, **pd_sli.dict()) for pd_sli in
                           request.sale_line_items]
        self.db.add_all(sale_line_items)
        self.db.commit()
        return sale_row.first()

    def delete(self, sale_id: int):
        sale_row = self._get(sale_id)

        # Update qty in items
        sli_rows = self.db.query(tables.SaleLineItem).filter(tables.SaleLineItem.sale_id == sale_id)
        for pd_sli in sli_rows:
            item_row = self.db.query(tables.Item).filter(tables.Item.id == pd_sli.item_id)
            item_pd = schemas_item.Item.from_orm(item_row.first())
            item_pd.qty += pd_sli.qty
            item_row.update(item_pd.dict())

        sale_row.delete(synchronize_session=False)
        list_rows_sli = self.db.query(tables.SaleLineItem).filter(tables.SaleLineItem.sale_id == sale_id)
        list_rows_sli.delete(synchronize_session=False)
        self.db.commit()


if __name__ == '__main__':
    sli_s = [(1, 3), (2, 2), (4, 20)]
    new_sli_s = [(2, 4), (3, 2), (4, 20)]
    items = [(1, 1), (2, 5), (3, 3), (4, 20), (5, 10)]
    d_sli_s, d_new_sli_s, d_items = dict(sli_s), dict(new_sli_s), dict(items)
    c_sli_s, c_new_sli_s = Counter(), Counter()
    for item_id, qty in d_sli_s.items():
        c_sli_s[item_id] += qty
    for item_id, qty in d_new_sli_s.items():
        c_new_sli_s[item_id] += qty
    item_ids = list(d_sli_s | d_new_sli_s)
    need_items = {item_id: d_items[item_id] for item_id in item_ids if c_sli_s[item_id] != c_new_sli_s[item_id]}
    for item_id, qty in need_items.items():
        qty += c_sli_s[item_id] - c_new_sli_s[item_id]
        d_items[item_id] = qty
    print(d_items)
