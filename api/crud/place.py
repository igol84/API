from .. import tables
from ..schemas import place as schemas
from .base import CRUDBase


class Place(CRUDBase[tables.Place, schemas.CreatePlace, schemas.BasePlace]):
    table = tables.Place

