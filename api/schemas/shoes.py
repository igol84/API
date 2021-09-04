from pydantic import BaseModel


class BaseShoes(BaseModel):
    id: int
    color: str
    size: float
    length: float
    width: str

class UpdateShoes(BaseModel):
    color: str
    size: float
    length: float
    width: str

class CreateShoes(BaseShoes):
    pass


class Shoes(BaseShoes):
    pass

    class Config:
        orm_mode = True
