from .base import CRUDBase
from .. import tables
from ..schemas import seller as schemas
from sqlalchemy import func


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

    def get_all_deletable(self, store_id: int) -> list[schemas.SellerWithDeletable]:
        db_obj = self.db.query(self.table.id, self.table.store_id, self.table.name, self.table.active,
                               tables.User.email, tables.User.role,
                               func.count(tables.Sale.seller_id).label("sales")) \
            .where(self.table.store_id == store_id) \
            .join(tables.User, self.table.id == tables.User.id, isouter=True)\
            .join(tables.Sale, self.table.id == tables.Sale.seller_id, isouter=True)\
            .group_by(self.table.id)
        return db_obj.all()
