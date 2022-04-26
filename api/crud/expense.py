from .. import tables
from ..schemas import expense as schemas
from .base import CRUDBase


class Expense(CRUDBase[tables.Expense, schemas.CreateExpense, schemas.BaseExpense]):
    table = tables.Expense

    def get_by_store_id(self, store_id: int) -> list[tables.Expense]:
        query = self.db.query(tables.Expense) \
            .where(tables.Expense.place_id == tables.Place.id) \
            .where(tables.Place.store_id == store_id).all()
        return query
