from typing import Optional

from pydantic import BaseModel

from .seller import Seller


class BaseUser(BaseModel):
    email: str
    password: str
    role: str


class CreateUser(BaseUser):
    id: int


class User(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    email: str
    seller: Seller

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    store_id: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: str
