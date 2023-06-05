from typing import Optional

from pydantic import BaseModel


class BaseShowcase(BaseModel):
    name: str
    color: str
    brand_id: Optional[int]
    title: Optional[str]
    title_ua: Optional[str]
    desc: Optional[str]
    desc_ua: Optional[str]
    url: str
    youtube: Optional[str]
    active: bool


class UpdateShowcase(BaseShowcase):
    pass


class CreateShowcase(BaseShowcase):
    pass


class Showcase(BaseShowcase):
    class Config:
        orm_mode = True


class ShowcaseDirs(BaseModel):
    name: str
    images: list[str]


class DelImgShowcase(BaseModel):
    dirName: str
    imgName: str
