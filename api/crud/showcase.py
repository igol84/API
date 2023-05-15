from .. import tables
from ..schemas import showcase as schemas
from .base import CRUDBase


class Showcase(CRUDBase[tables.Showcase, schemas.CreateShowcase, schemas.BaseShowcase]):
    table = tables.Showcase
