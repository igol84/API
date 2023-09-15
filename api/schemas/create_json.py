from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Optional

@dataclass
class Brand:
    name: str
    title: str
    title_ua: str
    desc: str
    desc_ua: str
    url: str
    active: bool

@dataclass
class Size:
    size: float
    length: Optional[float]
    price: float
    qty: int


@dataclass
class Product():
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

@dataclass
class All(DataClassJsonMixin):
    brands: list[Brand]
    products: list[str]
