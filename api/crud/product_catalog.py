from .. import tables
from ..schemas import product_catalog as schemas
from .base import CRUDBase


class ProductCatalog(CRUDBase[tables.ProductCatalog, schemas.CreateRowProductCatalog, schemas.BaseModel]):
    table = tables.ProductCatalog
    keys = ['store_id', 'prod_id']
    autoincrement = False
