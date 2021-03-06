from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, ForeignKey('sellers.id'), primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    seller = relationship('Seller', backref='users')


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desc = Column(String)
    sellers = relationship('Seller', backref='store')
    places = relationship('Place', backref='store')
    items = relationship('Item', backref='store')
    products_catalog = relationship('ProductCatalog', backref='store')


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    date_time = Column(DateTime, default=datetime.now)
    seller = relationship('Seller', backref='sales')
    place = relationship('Place', backref='sales')
    sale_line_items = relationship('SaleLineItem', back_populates='sale')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    price = Column(Float)
    shoes = relationship('Shoes', backref='product', uselist=False, cascade='all, delete')
    product_catalogs = relationship('ProductCatalog', back_populates='product')


class Shoes(Base):
    __tablename__ = "shoes"

    id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True, unique=True)
    color = Column(String)
    size = Column(Float)
    length = Column(Float)
    width = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    date_buy = Column(Date, default=date.today())
    prod_id = Column(Integer, ForeignKey('products.id'))
    qty = Column(Integer)
    buy_price = Column(Float)
    product = relationship('Product', backref='items')


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    name = Column(String)
    active = Column(Boolean, default=True)


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    name = Column(String)
    active = Column(Boolean, default=True)


class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    desc = Column(String)
    date_cost = Column(Date, default=date.today())
    cost = Column(Float)
    place = relationship('Place', backref='expenses')


class SaleLineItem(Base):
    __tablename__ = "sale_line_items"

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True, index=True)
    sale_price = Column(Float, primary_key=True, index=True)
    qty = Column(Integer)
    item = relationship('Item', backref='sale_line_items')
    sale = relationship('Sale', back_populates='sale_line_items')


class ProductCatalog(Base):
    __tablename__ = "product_catalogs"

    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True, index=True)
    prod_id = Column(Integer, ForeignKey('products.id'), primary_key=True, index=True)
    product = relationship('Product', back_populates='product_catalogs')
