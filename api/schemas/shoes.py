from typing import Optional

from pydantic import BaseModel


class BaseShoes(BaseModel):
    color: Optional[str]
    size: float
    length: Optional[float]
    width: Optional[str]


class UpdateShoes(BaseShoes):
    pass


class CreateShoes(BaseShoes):
    pass


class CreateShoesWithProduct(UpdateShoes):
    pass


class Shoes(BaseShoes):
    id: int

    class Config:
        orm_mode = True
