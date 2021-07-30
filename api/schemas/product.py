from pydantic import BaseModel


class BaseProduct(BaseModel):
    type: str
    name: str
    price: float


class CreateProduct(BaseProduct):
    pass


class Product(BaseProduct):
    id: int

    class Config:
        orm_mode = True
