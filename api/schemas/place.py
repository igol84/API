from pydantic import BaseModel


class BasePlace(BaseModel):
    store_id: int
    name: str


class CreatePlace(BasePlace):
    pass


class Place(BasePlace):
    id: int

    class Config:
        orm_mode = True
