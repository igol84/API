from pydantic import BaseModel


class BaseTagUrl(BaseModel):
    url: str
    search: str
    search_ua: str
    desc: str
    desc_ua: str


class CreateTagUrl(BaseTagUrl):
    pass


class UpdateTagUrl(BaseTagUrl):
    pass


class TagUrl(BaseTagUrl):
    class Config:
        orm_mode = True
