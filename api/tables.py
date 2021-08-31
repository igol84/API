from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    seller_id = Column(Integer)
    place_id = Column(Integer)
    date_time = Column(DateTime, default=datetime.now)

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


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    prod_id = Column(Integer, ForeignKey('products.id'))
    qty = Column(Integer)
    buy_price = Column(Float)
    product = relationship('Product', backref='items')


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    name = Column(String)


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    name = Column(String)


class SaleLineItem(Base):
    __tablename__ = "sale_line_items"

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True, index=True)
    sale_price = Column(Float, primary_key=True, index=True)
    qty = Column(Integer)
    item = relationship('Item', backref='sale_line_items')
    sale = relationship('Sale', backref='sale_line_items')

