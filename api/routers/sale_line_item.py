from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import sale_line_item as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['SaleLineItems'], prefix='/sale_line_item', dependencies=[Depends(get_current_user)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SaleLineItem)
def create(request: schemas.CreateSaleLineItem, sale_line_item: crud.SaleLineItem = Depends()):
    return sale_line_item.create(request)


@router.get('/', response_model=list[schemas.ShowSaleLineItemWithItem])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_sale_line_item: crud.SaleLineItem = Depends(),
            crud_shoes: crud.Shoes = Depends()):
    sale_line_items: list[schemas.ShowSaleLineItemWithItem] = crud_sale_line_item.get_all(skip, limit, search)
    for sale_line_item in sale_line_items:
        crud.product.set_product_details(sale_line_item.item.product, crud_shoes)
    return sale_line_items


@router.get('/{sale_id}/{item_id}/{sale_price}', status_code=200, response_model=schemas.ShowSaleLineItemWithItem)
def show(sale_id: int, item_id: int, sale_price: float, crud_sale_line_item: crud.SaleLineItem = Depends(),
         crud_shoes: crud.Shoes = Depends()):
    sale_line_item = crud_sale_line_item.get_sli(sale_id, item_id, sale_price)
    crud.product.set_product_details(sale_line_item.item.product, crud_shoes)
    return sale_line_item


@router.put('/{sale_id}/{item_id}/{sale_price}', status_code=status.HTTP_202_ACCEPTED,
            response_model=schemas.SaleLineItem)
def update(sale_id: int, item_id: int, sale_price: float,
           request: schemas.BaseSaleLineItem, sale_line_item: crud.SaleLineItem = Depends()):
    return sale_line_item.update_sli(sale_id, item_id, sale_price, request)


@router.delete('/{sale_id}/{item_id}/{sale_price')
def delete(sale_id: int, item_id: int, sale_price: float, sale_line_item: crud.SaleLineItem = Depends()):
    sale_line_item.delete_sli(sale_id, item_id, sale_price)
    return Response(status_code=status.HTTP_204_NO_CONTENT)