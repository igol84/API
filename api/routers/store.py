from fastapi import APIRouter, Depends, status, Response

from .. import crud
from .. schemas import store as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Stores'], prefix='/store', dependencies=[Depends(allow_create_resource)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Store)
def create(request: schemas.CreateStore, crud_store: crud.Store = Depends()):
    return crud_store.create(request)


@router.get('/', response_model=list[schemas.StoreWithDetails])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_store: crud.Store = Depends()):
    return crud_store.get_all(skip, limit, search)


@router.get('/{store_id}', status_code=200, response_model=schemas.StoreWithDetails)
def show(store_id: int, crud_store: crud.Store = Depends()):
    return crud_store.get(store_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Store)
def update(request: schemas.UpdateStore, crud_store: crud.Store = Depends()):
    return crud_store.update(request)


@router.delete('/{store_id}')
def delete(store_id: int, crud_store: crud.Store = Depends()):
    crud_store.delete(store_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
