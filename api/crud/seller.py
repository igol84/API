from .base import CRUDBase
from .. import tables
from ..schemas import seller as schemas


class Seller(CRUDBase[tables.Seller, schemas.CreateSeller, schemas.BaseSeller]):
    table = tables.Seller

    def edit_name(self, data: schemas.EditSellerName):
        seller = self.db.query(tables.Seller).filter(tables.Seller.id == data.seller_id)
        seller_row = seller.first()
        edited = False
        if seller_row.name != data.new_name:
            edited = True
            seller.update({'name': data.new_name})
        if edited:
            self.db.commit()
        return seller_row

    def edit_active(self, data: schemas.EditSellerActive):
        seller = self.db.query(tables.Seller).filter(tables.Seller.id == data.seller_id)
        seller_row = seller.first()
        edited = False
        if seller_row.active != data.active:
            edited = True
            seller.update({'active': data.active})
        if edited:
            self.db.commit()
        return seller_row
