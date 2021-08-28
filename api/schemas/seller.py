from pydantic import BaseModel


class BaseSeller(BaseModel):
    store_id: int
    name: str


class CreateSeller(BaseSeller):
    pass


class Seller(BaseSeller):
    id: int

    class Config:
        orm_mode = True
