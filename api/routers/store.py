from fastapi import APIRouter, Depends, status, Response

from .. import crud
from .. schemas import store as schemas
from ..auth2 import get_current_user


router = APIRouter(tags=['Stores'], prefix='/store', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Store)
def create(request: schemas.CreateStore, crud_store: crud.Store = Depends()):
    return crud_store.create(request)


@router.get('/', response_model=list[schemas.Store])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_store: crud.Store = Depends()):
    return crud_store.get_all(skip, limit, search)


@router.get('/{store_id}', status_code=200, response_model=schemas.Store)
def show(store_id: int, crud_store: crud.Store = Depends()):
    return crud_store.get(store_id)


@router.put('/{store_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Store)
def update(store_id: int, request: schemas.BaseStore, crud_store: crud.Store = Depends()):
    return crud_store.update(store_id, request)


@router.delete('/{store_id}')
def delete(store_id: int, crud_store: crud.Store = Depends()):
    crud_store.delete(store_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
