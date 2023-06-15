from dataclasses import dataclass
from typing import Optional


@dataclass
class Size:
    size: float
    length: str
    price: float


@dataclass
class Product:
    id: int
    type: str
    name: str
    name_ua: str
    category_id: int
    price: float
    images: list[str]
    brand: Optional[str]
    sizes: list[Size]
    desc: str
    desc_ua: str
    youtube: Optional[str]
