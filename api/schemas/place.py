from pydantic import BaseModel


class BasePlace(BaseModel):
    store_id: int
    name: str


class CreatePlace(BasePlace):
    pass


class UpdatePlace(BasePlace):
    id: int


class Place(BasePlace):
    id: int

    class Config:
        orm_mode = True
