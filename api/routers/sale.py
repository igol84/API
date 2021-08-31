from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import sale as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Sales'], prefix='/sale', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Sale)
def create(request: schemas.CreateSale, crud_sale: crud.Sale = Depends()):
    return crud_sale.create(request)


@router.get('/', response_model=list[schemas.ShowSaleWithSLIs])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_sale: crud.Sale = Depends(),
            crud_shoes: crud.Shoes = Depends()):
    sales: list[schemas.ShowSaleWithSLIs] = crud_sale.get_all(skip, limit, search)
    for sale in sales:
        for sli in sale.sale_line_items:
            crud.product.set_product_details(sli.item.product, crud_shoes)
    return sales


@router.get('/{sale_id}', status_code=200, response_model=schemas.ShowSaleWithSLIs)
def show(sale_id: int, crud_sale: crud.Sale = Depends(), crud_shoes: crud.Shoes = Depends()):
    sale: schemas.ShowSaleWithSLIs = crud_sale.get(sale_id)
    for sli in sale.sale_line_items:
        crud.product.set_product_details(sli.item.product, crud_shoes)
    return sale


@router.put('/{sale_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Sale)
def update(sale_id: int, request: schemas.BaseSale, crud_sale: crud.Sale = Depends()):
    return crud_sale.update(sale_id, request)


@router.delete('/{sale_id}')
def delete(sale_id: int, crud_sale: crud.Sale = Depends()):
    crud_sale.delete(sale_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
