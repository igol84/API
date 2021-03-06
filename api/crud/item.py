from .. import tables
from ..schemas import item as schemas
from .base import CRUDBase, HTTPException, status


class Item(CRUDBase[tables.Item, schemas.CreateItem, schemas.UpdateItem]):
    table = tables.Item

    def get_by_product_id(self, prod_id: int, skip: int = 0, limit: int = None) -> list[tables.Product]:
        EVEN = slice(skip, skip + limit) if limit else slice(skip, None)
        db_obj = self.db.query(self.table).where(self.table.prod_id == prod_id)
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} not contain \'{prod_id}\' prod_id')
        return db_obj[EVEN]
