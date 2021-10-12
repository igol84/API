from pydantic import BaseModel
from .product import Product


class CreateRowProductCatalog(BaseModel):
    store_id: int
    prod_id: int


class RowProductCatalog(CreateRowProductCatalog):
    class Config:
        orm_mode = True


class ShowRowProductCatalogWithProduct(RowProductCatalog):
    product: Product


class ProductCatalog(BaseModel):
    __root__: list[ShowRowProductCatalogWithProduct]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)