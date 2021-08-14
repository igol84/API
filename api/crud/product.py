from .. import tables
from ..schemas import product as schemas
from .base import CRUDBase


class Product(CRUDBase[tables.Product, schemas.CreateProduct, schemas.BaseProduct]):
    table = tables.Product
    search_columns = ['name']
