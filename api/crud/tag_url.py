from .. import tables
from ..schemas import tag_url as schemas
from .base import CRUDBase


class TagUrl(CRUDBase[tables.TagUrl, schemas.CreateTagUrl, schemas.BaseTagUrl]):
    table = tables.TagUrl
    keys = ['url']
