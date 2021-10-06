from .. import tables
from ..schemas import product as schemas
from .base import CRUDBase


class Product(CRUDBase[tables.Product, schemas.CreateProduct, schemas.BaseProduct]):
    table = tables.Product
    search_columns = ['name']

    def create(self, request: schemas.CreateProduct) -> tables.Product:
        components = {'shoes': tables.Shoes}
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
