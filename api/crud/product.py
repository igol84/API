from .. import tables
from ..schemas import product as schemas
from .base import CRUDBase
from .shoes import Shoes


def set_product_details(product: schemas.Product, crud_shoes: Shoes) -> schemas.Product:
    if product.type == 'shoes':
        product.shoes = crud_shoes.get(product.id)
    return product


class Product(CRUDBase[tables.Product, schemas.CreateProduct, schemas.BaseProduct]):
    table = tables.Product
    search_columns = ['name']
