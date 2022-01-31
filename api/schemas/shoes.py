from typing import Optional

from pydantic import BaseModel


class BaseShoes(BaseModel):
    id: int
    color: Optional[str]
    size: float
    length: Optional[float]
    width: Optional[str]


class UpdateShoes(BaseModel):
    color: Optional[str]
    size: float
    length: Optional[float]
    width: Optional[str]


class CreateShoes(BaseShoes):
    pass


class CreateShoesWithProduct(UpdateShoes):
    pass


class Shoes(BaseShoes):
    pass

    class Config:
        orm_mode = True
