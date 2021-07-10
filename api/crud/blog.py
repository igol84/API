from .. import tables
from ..schemas import blog as schemas
from .base import CRUDBase


class Blog(CRUDBase[tables.Blog, schemas.CreateBlog, schemas.UpdateBlog]):
    table = tables.Blog

    def create_blog(self, request: schemas.CreateBlog, user_id: int) -> tables.Blog:
        data = request.dict()
        data['user_id'] = user_id
        return self.create(data)
