from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import item as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Items'], prefix='/item', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowItemWithProduct)
def create(request: schemas.CreateItem, crud_item: crud.Item = Depends()):
    return crud_item.create(request)


@router.get('/', response_model=list[schemas.ShowItemWithProduct])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_item: crud.Item = Depends()):
    return crud_item.get_all(skip, limit, search)


@router.get('/{item_id}', status_code=200, response_model=schemas.ShowItemWithProduct)
def show(item_id: int, crud_item: crud.Item = Depends()):
    return crud_item.get(item_id)


@router.get('/by_prod_id/{prod_id}', status_code=200, response_model=list[schemas.ShowItemWithProduct])
def get_items_by_product_id(prod_id: int, skip: int = None, limit: int = None, crud_item: crud.Item = Depends()):
    return crud_item.get_by_product_id(prod_id, skip, limit)


@router.get('/by_store_id/{store_id}', status_code=200, response_model=list[schemas.ShowItemWithProduct])
def get_items_by_store_id(store_id: int, crud_item: crud.Item = Depends()):
    return crud_item.get_items_by_store_id(store_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowItemWithProduct)
def update(request: schemas.UpdateItem, crud_item: crud.Item = Depends()):
    return crud_item.update(request)


@router.delete('/{item_id}')
def delete(item_id: int, crud_item: crud.Item = Depends()):
    crud_item.delete(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
