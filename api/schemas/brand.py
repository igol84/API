from typing import Optional

from pydantic import BaseModel


class BaseBrand(BaseModel):
    name: str
    title: Optional[str]
    title_ua: Optional[str]
    desc: Optional[str]
    desc_ua: Optional[str]
    url: str
    active: bool


class CreateBrand(BaseBrand):
    pass


class UpdateBrand(CreateBrand):
    id: int


class Brand(BaseBrand):
    id: int

    class Config:
        orm_mode = True
