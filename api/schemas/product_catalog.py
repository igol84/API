from pydantic import BaseModel
from .product import Product


class CreateProductCatalog(BaseModel):
    store_id: int
    prod_id: int


class ProductCatalog(CreateProductCatalog):
    class Config:
        orm_mode = True


class ShowProductCatalogWithProduct(ProductCatalog):
    product: Product
