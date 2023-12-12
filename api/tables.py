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


class Showcase(Base):
    __tablename__ = "showcase"
    key = Column(String, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    brand_id = Column(Integer)
    title = Column(String)
    title_ua = Column(String)
    desc = Column(String)
    desc_ua = Column(String)
    url = Column(String)
    youtube = Column(String)
    active = Column(Boolean)
    prom_active = Column(Boolean)
    images = relationship('ShowcaseImage', back_populates='showcase', cascade='all, delete')
    date = Column(Date, default=date.today())
    tags = Column(String, server_default="")


class ShowcaseImage(Base):
    __tablename__ = "showcase_image"
    dir = Column(String, ForeignKey('showcase.key'), primary_key=True, index=True)
    image = Column(String, primary_key=True, index=True)
    showcase = relationship('Showcase', back_populates='images')


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    title_ua = Column(String)
    desc = Column(String)
    desc_ua = Column(String)
    url = Column(String)
    active = Column(Boolean)


class TagUrl(Base):
    __tablename__ = "tag_url"
    url = Column(String, primary_key=True, index=True)
    parent = Column(String, server_default="")
    order_number = Column(Integer, server_default="0")
    search = Column(String)
    search_ua = Column(String)
    desc = Column(String)
    desc_ua = Column(String)
    text = Column(String)
    text_ua = Column(String)
