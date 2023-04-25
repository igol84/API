from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import expense as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Expense'], prefix='/expense', dependencies=[Depends(get_current_user)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Expense)
def create(request: schemas.CreateExpense, crud_expense: crud.Expense = Depends()):
    return crud_expense.create(request)


@router.get('/', response_model=list[schemas.Expense])
def get_all(skip: int = None, limit: int = None, store_id: int = None, crud_expense: crud.Expense = Depends()):
    return crud_expense.get_all(skip, limit, store_id)


@router.get('/{expense_id}', status_code=200, response_model=schemas.Expense)
def show(expense_id: int, crud_expense: crud.Expense = Depends()):
    return crud_expense.get(expense_id)


@router.get('/get_by_store_id/{store_id}', response_model=list[schemas.Expense])
def get_by_store_id(store_id: int, crud_expense: crud.Expense = Depends()):
    return crud_expense.get_by_store_id(store_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Expense)
def update(request: schemas.UpdateExpense, crud_expense: crud.Expense = Depends()):
    return crud_expense.update(request)


@router.delete('/{expense_id}')
def delete(expense_id: int, crud_expense: crud.Expense = Depends()):
    crud_expense.delete(expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
