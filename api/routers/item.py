from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import item as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Items'], prefix='/item', dependencies=[Depends(get_current_user)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create(request: schemas.CreateItem, crud_item: crud.Item = Depends()):
    return crud_item.create(request)


@router.get('/', response_model=list[schemas.ShowItemWithProduct])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_item: crud.Item = Depends(),
            crud_shoes: crud.Shoes = Depends()):
    items: list[schemas.ShowItemWithProduct] = crud_item.get_all(skip, limit, search)
    for item in items:
        if item.product.type == 'shoes':
            item.product.shoes = crud_shoes.get(item.product.id)
    return items


@router.get('/{item_id}', status_code=200, response_model=schemas.ShowItemWithProduct)
def show(item_id: int, crud_item: crud.Item = Depends(), crud_shoes: crud.Shoes = Depends()):
    item: schemas.ShowItemWithProduct = crud_item.get(item_id)
    if item.product.type == 'shoes':
        item.product.shoes = crud_shoes.get(item.prod_id)
    return item


@router.get('/by_prod_id/{prod_id}', status_code=200, response_model=list[schemas.Item])
def get_all_by_user_id(prod_id: int, skip: int = None, limit: int = None, crud_item: crud.Item = Depends()):
    return crud_item.get_by_product_id(prod_id, skip, limit)


@router.put('/{item_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Item)
def update(item_id: int, request: schemas.BaseItem, crud_item: crud.Item = Depends()):
    return crud_item.update(item_id, request)


@router.delete('/{item_id}')
def delete(item_id: int, crud_item: crud.Item = Depends()):
    crud_item.delete(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
