from typing import Optional

from pydantic import BaseModel


class LightShowcase(BaseModel):
    url: str

    class Config:
        orm_mode = True


class BaseShowcaseImage(BaseModel):
    dir: str
    image: str


class ShowcaseImage(BaseShowcaseImage):
    class Config:
        orm_mode = True


class BaseShowcase(BaseModel):
    key: str
    name: str
    color: str
    brand_id: Optional[int]
    title: Optional[str]
    title_ua: Optional[str]
    desc: Optional[str]
    desc_ua: Optional[str]
    url: str
    youtube: Optional[str]
    active: bool
    prom_active: bool


class CreateShowcase(BaseShowcase):
    images: list[BaseShowcaseImage] = []


class UpdateShowcase(CreateShowcase):
    pass


class Showcase(BaseShowcase):
    images: list[ShowcaseImage] = []

    class Config:
        orm_mode = True


class ShowcaseDirs(BaseModel):
    name: str
    images: list[str]


class DelImgShowcase(BaseModel):
    dirName: str
    imgName: str


class DelShowcase(BaseModel):
    pass


class Size(BaseModel):
    size: float
    length: Optional[float]
    price: float
    qty: int


class Product(BaseModel):
    id: int
    type: str
    product_key: str
    name: str
    name_ua: str
    url: str
    qty: Optional[int]
    brand_id: int
    price: float
    images: list[str]
    brand: Optional[str]
    sizes: list[Size]
    desc: str
    desc_ua: str
    youtube: Optional[str]
