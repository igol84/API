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


class ListPlace(BaseModel):
    __root__: list[Place]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
