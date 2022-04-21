from .. import tables
from ..schemas import expense as schemas
from .base import CRUDBase


class Expense(CRUDBase[tables.Expense, schemas.CreateExpense, schemas.BaseExpense]):
    table = tables.Expense
