from typing import Optional

from pydantic import BaseModel


class BaseShowcase(BaseModel):
    name: str
    title: Optional[str]
    desc: Optional[str]
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
