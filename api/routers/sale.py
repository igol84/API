from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import sale as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Sales'], prefix='/sale', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowSaleWithSLIs)
def create(request: schemas.CreateSale, crud_sale: crud.Sale = Depends()):
    return crud_sale.create(request)


@router.get('/', response_model=list[schemas.ShowSaleWithSLIs])
def get_all(skip: int = None, limit: int = None, date: str = None, crud_sale: crud.Sale = Depends()):
    return crud_sale.get_all(skip, limit, date)


@router.get('/{sale_id}', status_code=200, response_model=schemas.ShowSaleWithSLIs)
def show(sale_id: int, crud_sale: crud.Sale = Depends()):
    return crud_sale.get(sale_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowSaleWithSLIs)
def update(request: schemas.UpdateSale, crud_sale: crud.Sale = Depends()):
    return crud_sale.update(request)


@router.delete('/{sale_id}')
def delete(sale_id: int, crud_sale: crud.Sale = Depends()):
    crud_sale.delete(sale_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
