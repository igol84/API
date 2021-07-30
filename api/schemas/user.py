from typing import Optional

from pydantic import BaseModel
from .product import Product


class BaseUser(BaseModel):
    name: str
    email: str
    password: str


class CreateUser(BaseUser):
    pass


class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    email: Optional[str] = None
