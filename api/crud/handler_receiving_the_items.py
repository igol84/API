import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.handler_receiving_the_items import ModelProduct
from ..schemas.item import CreateItem
from ..schemas.product import CreateProduct
from ..schemas.product_catalog import CreateRowProductCatalog
from ..schemas.shoes import CreateShoesWithProduct


class HeaderReceivingTheItems:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def receiving_the_items(self, data: ModelProduct) -> None:
        if data.type.name == 'product':
            if data.id:
                # create new item
                pd_item = CreateItem(prod_id=data.id, store_id=data.store_id, qty=data.qty,
                                     buy_price=data.price_buy, date_buy=datetime.date.today())
                new_item = tables.Item(**pd_item.dict())
                self.db.add(new_item)
                self.db.commit()
            else:
                # create new product and item
                # check product available by name
                product = self.db.query(tables.Product).filter(
                    tables.Product.name == data.name,
                    tables.Product.type == data.type.name).first()
                if not product:
                    pd_product = CreateProduct(type=data.type.name, name=data.name, price=data.price_sell)
                    product = tables.Product(**pd_product.dict())
                    self.db.add(product)
                    self.db.commit()
                    self.db.refresh(product)
                    pd_pc = CreateRowProductCatalog(store_id=data.store_id, prod_id=product.id)
                    pc = tables.ProductCatalog(**pd_pc.dict())
                    self.db.add(pc)
                    self.db.commit()
                # create new item
                pd_item = CreateItem(prod_id=product.id, store_id=data.store_id, qty=data.qty,
                                     buy_price=data.price_buy, date_buy=datetime.date.today())
                new_item = tables.Item(**pd_item.dict())
                self.db.add(new_item)
                self.db.commit()
        elif data.type.name == 'shoes':
            products = self.db.query(tables.ProductCatalog, tables.Product, tables.Shoes).filter(
                tables.ProductCatalog.store_id == data.store_id,
                tables.ProductCatalog.prod_id == tables.Product.id,
                tables.Product.id == tables.Shoes.id,
                tables.Product.name == data.name,
                tables.Shoes.color == data.module.color,
                tables.Shoes.width == data.module.width).all()
            db_sizes = {(shoes.size, shoes.length): {'id': product.id} for pc, product, shoes in products}

            for pd_size in data.module.sizes:
                key = (pd_size.size, pd_size.length)
                if key in db_sizes:
                    # create new item for product.shoes id:', result.prod_id

                    pd_item = CreateItem(prod_id=db_sizes[key]['id'], store_id=data.store_id, qty=pd_size.qty,
                                         buy_price=data.price_buy, date_buy=datetime.date.today())
                    new_item = tables.Item(**pd_item.dict())
                    self.db.add(new_item)
                    self.db.commit()
                else:
                    pd_product = CreateProduct(type=data.type.name, name=data.name, price=data.price_sell)
                    pd_shoes = CreateShoesWithProduct(color=data.module.color, size=pd_size.size, length=pd_size.length,
                                                      width=data.module.width)
                    pd_product.shoes = tables.Shoes(**pd_shoes.dict())
                    product = tables.Product(**pd_product.dict())
                    self.db.add(product)
                    self.db.commit()
                    self.db.refresh(product)
                    pd_pc = CreateRowProductCatalog(store_id=data.store_id, prod_id=product.id)
                    pc = tables.ProductCatalog(**pd_pc.dict())
                    self.db.add(pc)
                    pd_item = CreateItem(prod_id=product.id, store_id=data.store_id, qty=pd_size.qty,
                                         buy_price=data.price_buy, date_buy=datetime.date.today())
                    new_item = tables.Item(**pd_item.dict())
                    self.db.add(new_item)
                    self.db.commit()