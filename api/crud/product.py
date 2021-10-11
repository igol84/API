from fastapi import HTTPException, status

from .. import tables
from ..schemas import product as schemas
from .base import CRUDBase


class Product(CRUDBase[tables.Product, schemas.CreateProduct, schemas.BaseProduct]):
    table = tables.Product
    search_columns = ['name']
    components = {'shoes': tables.Shoes}

    def create(self, request: schemas.CreateProduct) -> tables.Product:
        components = self.components
        product_row = self.table(**request.dict(exclude=components.keys()))
        # product_row.shoes = tables.Shoes(**request.shoes.dict()) ->
        for component in components:
            if request.type == component and request.__dict__[component]:
                setattr(product_row, component, components[component](**request.__dict__[component].dict()))
                break
        self.db.add(product_row)
        self.db.commit()
        self.db.refresh(product_row)
        return product_row

    def update(self, request: schemas.Product) -> tables.Product:
        product_db_row = self._get(request.id)
        old_product_row: tables.Product = product_db_row.first()
        components = self.components
        # delete old component
        for component in components:
            if old_product_row.type == component:
                db_obj = self.db.query(components[component]).filter(components[component].id == request.id)
                if not db_obj.first():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'{components[component].__name__} with the id \'{request.id}\' is not available')
                db_obj.delete(synchronize_session=False)
                break
        # update product without component
        product_db_row.update(request.dict(exclude=components.keys()))
        # add new component
        for component in components:
            if request.type == component and request.__dict__[component]:
                setattr(old_product_row, component, components[component](**request.__dict__[component].dict()))
                break
        self.db.commit()
        return product_db_row.first()
