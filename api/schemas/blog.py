from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    body: str


class CreateBlog(BaseBlog):
    pass


class Blog(BaseBlog):
    id: int

    class Config:
        orm_mode = True


class UpdateBlog(BaseBlog):
    pass


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowBlogTitle(BaseModel):
    title: str

    class Config:
        orm_mode = True

from .user import ShowUser
class ShowBlogWithCreator(ShowBlog):
    creator: ShowUser

