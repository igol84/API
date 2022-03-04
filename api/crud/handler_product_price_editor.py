from fastapi import Depends
from sqlalchemy.orm import Session

from .. import database
from .. import tables
from ..schemas.handler_product_price_editor import ModelProduct


class HandlerProductPriceEditor:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def edit_product(self, data: ModelProduct) -> None:
        product = self.db.query(tables.Product).filter(
            tables.Product.id == data.id)
        product.update({'price': data.price_for_sale})
        product = product.first()
        self.db.commit()
        return ModelProduct(id=product.id, price_for_sale=product.price)
