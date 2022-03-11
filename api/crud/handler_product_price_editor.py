from fastapi import Depends
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas import handler_product_price_editor as schemas


class HandlerProductPriceEditor:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_product(self, data: schemas.ModelProduct) -> schemas.ModelProduct:
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
        product_row = product.first()
        if edited:
            self.db.commit()
        return schemas.ModelProduct(id=product_row.id, price_for_sale=product_row.price, size=product_row.shoes.size)

    def edit_shoes(self, shoes_form: schemas.ModelShoes) -> schemas.ModelShoes:
        if shoes_form.name != shoes_form.new_name or shoes_form.price_for_sale is not None:
            products = self.db.query(tables.Product).filter(tables.Product.name == shoes_form.name)
            if shoes_form.name != shoes_form.new_name:
                products.update({'name': shoes_form.new_name})
            if shoes_form.price_for_sale is not None:
                products.update({'price': shoes_form.price_for_sale})
            self.db.commit()
        return schemas.ModelShoes(name=shoes_form.name, new_name=shoes_form.new_name,
                                  price_for_sale=shoes_form.price_for_sale)

    def edit_color(self, color_form: schemas.ModelColor) -> None:
        if color_form.color != color_form.new_color or color_form.price_for_sale is not None:
            query = self.db.query(tables.Product, tables.Shoes).\
                filter(tables.Product.id == tables.Shoes.id).\
                filter(tables.Product.name == color_form.name).\
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
        return schemas.ModelColor(name=color_form.name, color=color_form.color, new_color=color_form.new_color,
                                  price_for_sale=color_form.price_for_sale)
