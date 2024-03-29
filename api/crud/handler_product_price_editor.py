from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import database
from .. import tables
from ..schemas import handler_product_price_editor as schemas


class HandlerProductPriceEditor:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_product(self, data: schemas.ModelProductForm) -> schemas.ModelProductForm:
        product = self.db.query(tables.Product).filter(tables.Product.id == data.id)
        product_row = product.first()
        edited = False
        if product_row.price != data.new_price:
            edited = True
            product.update({'price': data.new_price})
        if product_row.name != data.new_name:
            edited = True
            product.update({'name': data.new_name})
        product_row = product.first()
        if edited:
            self.db.commit()
        return schemas.ModelProductForm(id=product_row.id, new_name=product_row.name, new_price=product_row.price)

    def edit_size(self, data: schemas.ModelSizeForm) -> schemas.ModelSizeForm:
        product = self.db.query(tables.Product).filter(tables.Product.id == data.id)
        product_row = product.first()
        edited = False
        if product_row.price != data.price_for_sale:
            edited = True
            product.update({'price': data.price_for_sale})
        if product_row.shoes.size != data.size:
            edited = True
            shoes = self.db.query(tables.Shoes).filter(tables.Shoes.id == data.id)
            shoes.update({'size': data.size})
        if product_row.shoes.length != data.length:
            edited = True
            shoes = self.db.query(tables.Shoes).filter(tables.Shoes.id == data.id)
            shoes.update({'length': data.length})
        product_row = product.first()
        if edited:
            self.db.commit()
        return schemas.ModelSizeForm(id=product_row.id, price_for_sale=product_row.price, size=product_row.shoes.size,
                                     length=product_row.shoes.length)

    def edit_shoes(self, shoes_form: schemas.ModelShoesForm) -> schemas.ModelShoesForm:
        if shoes_form.name != shoes_form.new_name or shoes_form.price_for_sale is not None:
            update_data = {}
            query = self.db.query(tables.Product).filter(
                func.lower(tables.Product.name) == func.lower(shoes_form.name))
            ids = [product.id for product in query]

            if shoes_form.name != shoes_form.new_name:
                update_data['name'] = shoes_form.new_name
            if shoes_form.price_for_sale is not None:
                update_data['price'] = shoes_form.price_for_sale
            products = self.db.query(tables.Product).filter(tables.Product.id.in_(ids))
            products.update(update_data)
            self.db.commit()

        return schemas.ModelShoesForm(name=shoes_form.name, new_name=shoes_form.new_name,
                                      price_for_sale=shoes_form.price_for_sale)

    def edit_color(self, color_form: schemas.ModelColorForm) -> None:
        if color_form.color != color_form.new_color or color_form.price_for_sale is not None:
            query = self.db.query(tables.Product, tables.Shoes). \
                filter(tables.Product.id == tables.Shoes.id). \
                filter(func.lower(tables.Product.name) == func.lower(color_form.name)). \
                filter(tables.Shoes.color == color_form.color)
            ids = [product.id for product, shoes_color in query]

            # update color
            if color_form.color != color_form.new_color:
                shoes = self.db.query(tables.Shoes).filter(tables.Shoes.id.in_(ids))
                shoes.update({'color': color_form.new_color})

            # update price
            if color_form.price_for_sale is not None:
                products = self.db.query(tables.Product).filter(tables.Product.id.in_(ids))
                products.update({'price': color_form.price_for_sale})

            self.db.commit()
        return schemas.ModelColorForm(name=color_form.name, color=color_form.color, new_color=color_form.new_color,
                                      price_for_sale=color_form.price_for_sale)
