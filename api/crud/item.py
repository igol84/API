from .. import tables
from ..schemas import item as schemas
from .base import CRUDBase


class Item(CRUDBase[tables.Item, schemas.CreateItem, schemas.BaseItem]):
    table = tables.Item
