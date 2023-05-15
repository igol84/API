from typing import Optional

from pydantic import BaseModel


class BaseShowcase(BaseModel):
    id: int
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
    pass

    class Config:
        orm_mode = True
