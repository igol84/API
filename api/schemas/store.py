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
