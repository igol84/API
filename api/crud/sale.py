from .. import tables
from ..schemas import sale as schemas
from .base import CRUDBase


class Sale(CRUDBase[tables.Sale, schemas.CreateSale, schemas.BaseSale]):
    table = tables.Sale
