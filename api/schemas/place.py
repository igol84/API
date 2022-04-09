from pydantic import BaseModel


class BasePlace(BaseModel):
    store_id: int
    name: str
    active: bool


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

class EditPlaceName(BaseModel):
    place_id: int
    new_name: str


class EditPlaceActive(BaseModel):
    place_id: int
    active: bool