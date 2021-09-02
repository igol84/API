from pydantic import BaseModel


class BaseStore(BaseModel):
    name: str
    desc: str


class CreateStore(BaseStore):
    pass


class Store(BaseStore):
    id: int

    class Config:
        orm_mode = True


from .seller import Seller
from .place import Place
from .item import ShowItemWithProduct


class StoreWithDetails(Store):
    sellers: list[Seller]
    places: list[Place]
    items: list[ShowItemWithProduct]
