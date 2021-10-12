from sqlalchemy import or_
from .. import tables
from ..schemas import product_catalog as schemas
from .base import CRUDBase


class ProductCatalog(CRUDBase[tables.ProductCatalog, schemas.CreateRowProductCatalog, schemas.BaseModel]):
    table = tables.ProductCatalog
    keys = ['store_id', 'prod_id']
    autoincrement = False

    def get_store_pc(
            self, store_id: int, skip: int = 0, limit: int = None,
            q_search: str = None) -> list[tables.ProductCatalog]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table).filter(self.table.store_id == store_id)

        if self.search_columns and q_search:
            search = []
            for column in self.search_columns:
                search.append(getattr(self.table, column).ilike(f'%{q_search}%'))
            db_obj = db_obj.filter(or_(*search))
        return db_obj[SLICE]
