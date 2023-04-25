from .. import tables
from ..schemas import expense as schemas
from .base import CRUDBase


class Expense(CRUDBase[tables.Expense, schemas.CreateExpense, schemas.BaseExpense]):
    table = tables.Expense

    def get_all(self, skip: int = 0, limit: int = None, store_id: int = None) -> list[table]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table)
        if store_id:
            db_obj = db_obj \
                .where(tables.Expense.place_id == tables.Place.id) \
                .where(tables.Place.store_id == store_id)

        return db_obj[SLICE]

    def get_by_store_id(self, store_id: int) -> list[tables.Expense]:
        query = self.db.query(tables.Expense) \
            .where(tables.Expense.place_id == tables.Place.id) \
            .where(tables.Place.store_id == store_id).all()
        return query
