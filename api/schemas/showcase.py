from typing import Optional

from pydantic import BaseModel


class BaseShowcase(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    url: str
    youtube: Optional[str]
    active: bool


class UpdateShowcase(BaseShowcase):
    id: int


class CreateShowcase(BaseShowcase):
    pass


class Showcase(BaseShowcase):
    id: int

    class Config:
        orm_mode = True
