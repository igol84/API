from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import product as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
allow_read_resource = RoleChecker(["admin", "user"])
router = APIRouter(tags=['Products'], prefix='/prod')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Product,
             dependencies=[Depends(allow_create_resource)])
def create(request: schemas.CreateProduct, crud_prod: crud.Product = Depends()):
    return crud_prod.create(request)


@router.get('/', response_model=list[schemas.Product],
            dependencies=[Depends(allow_read_resource)])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_product: crud.Product = Depends()):
    return crud_product.get_all(skip, limit, search)


@router.get('/{prod_id}', status_code=200, response_model=schemas.Product,
            dependencies=[Depends(allow_read_resource)])
def show(prod_id: int, crud_prod: crud.Product = Depends()):
    return crud_prod.get(prod_id)


@router.put('/{prod_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Product,
            dependencies=[Depends(allow_create_resource)])
def update(prod_id: int, request: schemas.UpdateProduct, crud_prod: crud.Product = Depends()):
    return crud_prod.update(prod_id, request)


@router.delete('/{prod_id}', dependencies=[Depends(allow_create_resource)])
def delete(prod_id: int, crud_prod: crud.Product = Depends(), crud_shoes: crud.Shoes = Depends()):
    product: schemas.Product = crud_prod.get(prod_id)
    if product.type == 'shoes':
        if crud_shoes.is_id_exist(prod_id):
            crud_shoes.delete(prod_id)
    crud_prod.delete(prod_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
