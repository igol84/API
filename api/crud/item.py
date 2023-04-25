from .. import tables
from ..schemas import item as schemas
from .base import CRUDBase, HTTPException, status


class Item(CRUDBase[tables.Item, schemas.CreateItem, schemas.UpdateItem]):
    table = tables.Item

    def get_all(self, skip: int = 0, limit: int = None, store_id: int = None, prod_id: int = None) -> list[table]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table)
        if store_id:
            db_obj = db_obj.from_self().where(self.table.store_id == store_id)
        if prod_id:
            db_obj = db_obj.where(self.table.prod_id == prod_id)
        return db_obj[SLICE]

    def get_by_product_id(self, prod_id: int, skip: int = 0, limit: int = None) -> list[tables.Item]:
        EVEN = slice(skip, skip + limit) if limit else slice(skip, None)
        db_obj = self.db.query(self.table).where(self.table.prod_id == prod_id)
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} not contain \'{prod_id}\' prod_id')
        return db_obj[EVEN]

    def get_items_by_store_id(self, store_id: int) -> list[tables.Product]:
        db_obj = self.db.query(self.table).where(self.table.store_id == store_id)
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} not contain \'{store_id}\' store_id')
        return db_obj.all()
