from .. import tables
from ..schemas import store as schemas
from .base import CRUDBase


class Store(CRUDBase[tables.Store, schemas.CreateStore, schemas.BaseStore]):
    table = tables.Store

