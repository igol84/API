from .. import tables
from ..schemas import shoes as schemas
from .base import CRUDBase


class Shoes(CRUDBase[tables.Shoes, schemas.CreateShoes, schemas.BaseShoes]):
    table = tables.Shoes

