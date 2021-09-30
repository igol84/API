from .. import tables
from ..schemas import product_catalog as schemas
from .base import CRUDBase, HTTPException, status


class ProductCatalog(CRUDBase[tables.ProductCatalog, schemas.CreateProductCatalog, schemas.BaseModel]):
    table = tables.ProductCatalog
    schema = schemas.BaseModel

    def _get_product_catalog(self, store_id: int, prod_id: int):
        db_obj = self.db.query(self.table).filter(
            self.table.store_id == store_id,
            self.table.prod_id == prod_id,
        )
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} with the store_id \'{store_id}\''
                                       f' and prod_id \'{prod_id}\' is not available')
        return db_obj

    def get_product_catalog(self, store_id: int, prod_id: int) -> table:
        return self._get_product_catalog(store_id, prod_id).first()

    def update_product_catalog(self, store_id: int, prod_id: int, request: schema) -> table:
        db_obj = self._get_product_catalog(store_id, prod_id)
        db_obj.update(request.dict())
        self.db.commit()
        return db_obj.first()

    def delete_product_catalog(self, store_id: int, prod_id: int):
        db_obj = self._get_product_catalog(store_id, prod_id)
        db_obj.delete(synchronize_session=False)
        self.db.commit()
