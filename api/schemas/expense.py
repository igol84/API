import datetime

from pydantic import BaseModel


class BaseExpense(BaseModel):
    place_id: int
    desc: str
    date_cost: datetime.date
    cost: float


class CreateExpense(BaseExpense):
    pass


class UpdateExpense(CreateExpense):
    id: int


class Expense(BaseExpense):
    id: int

    class Config:
        orm_mode = True
