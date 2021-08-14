from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    price = Column(Float)


class Shoes(Base):
    __tablename__ = "shoes"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    color = Column(String)
    size = Column(Float)
    length = Column(Float)
    width = Column(String)
