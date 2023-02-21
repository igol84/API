from typing import Optional

from pydantic import BaseModel


class BaseSeller(BaseModel):
    store_id: int
    name: str
    active: bool


class CreateSeller(BaseSeller):
    pass


class UpdateSeller(CreateSeller):
    id: int


class Seller(BaseSeller):
    id: int

    class Config:
        orm_mode = True

class SellerDeletable(BaseSeller):
    id: int

    class Config:
        orm_mode = True


class EditSellerName(BaseModel):
    seller_id: int
    new_name: str


class EditSellerActive(BaseModel):
    seller_id: int
    active: bool

class SellerWithDeletable(BaseModel):
    store_id: int
    id: int
    name: str
    active: bool
    email: Optional[str]
    role: Optional[str]
    sales: int
