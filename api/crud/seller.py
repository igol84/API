from .. import tables
from ..schemas import seller as schemas
from .base import CRUDBase


class Seller(CRUDBase[tables.Seller, schemas.CreateSeller, schemas.BaseSeller]):
    table = tables.Seller

