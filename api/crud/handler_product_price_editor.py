from fastapi import Depends
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.handler_product_price_editor import ModelProduct


class HandlerProductPriceEditor:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_product(self, data: ModelProduct) -> None:
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
        return ModelProduct(id=product_row.id, price_for_sale=product_row.price, size=product_row.shoes.size)
