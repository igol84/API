from pydantic import BaseModel


class BaseTagUrl(BaseModel):
    url: str
    parent: str
    order_number: int
    search: str
    search_ua: str
    desc: str
    desc_ua: str
    text: str
    text_ua: str


class CreateTagUrl(BaseTagUrl):
    pass


class UpdateTagUrl(BaseTagUrl):
    pass


class TagUrl(BaseTagUrl):
    class Config:
        orm_mode = True
