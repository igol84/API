from fastapi import APIRouter, Depends, status, Response

from .. import crud
from .. schemas import shoes as schemas
from ..auth2 import get_current_user


router = APIRouter(tags=['Shoes'], prefix='/shoes', dependencies=[Depends(get_current_user)])#


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Shoes)
def create(request: schemas.CreateShoes, crud_shoes: crud.Shoes = Depends()):
    return crud_shoes.create(request)


@router.get('/', response_model=list[schemas.Shoes])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_shoes: crud.Shoes = Depends()):
    return crud_shoes.get_all(skip, limit, search)


@router.get('/{shoes_id}', status_code=200, response_model=schemas.Shoes)
def show(shoes_id: int, crud_shoes: crud.Shoes = Depends()):
    return crud_shoes.get(shoes_id)


@router.put('/{shoes_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Shoes)
def update(shoes_id: int, request: schemas.BaseShoes, crud_shoes: crud.Shoes = Depends()):
    return crud_shoes.update(shoes_id, request)


@router.delete('/{shoes_id}')
def delete(shoes_id: int, crud_shoes: crud.Shoes = Depends(),  crud_prod: crud.Product = Depends()):
    crud_shoes.delete(shoes_id)
    if crud_prod.is_id_exist(shoes_id):
        crud_prod.delete(shoes_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
