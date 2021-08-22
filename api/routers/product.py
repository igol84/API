from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import product as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Products'], prefix='/prod', dependencies=[Depends(get_current_user)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create(request: schemas.CreateProduct, crud_prod: crud.Product = Depends()):
    return crud_prod.create(request)


@router.get('/', response_model=list[schemas.Product])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_blog: crud.Product = Depends(),
            crud_shoes: crud.Shoes = Depends()):
    products: list[schemas.Product] = crud_blog.get_all(skip, limit, search)
    for product in products:
        if product.type == 'shoes':
            product.shoes = crud_shoes.get(product.id)
    return products


@router.get('/{prod_id}', status_code=200, response_model=schemas.Product)
def show(prod_id: int, crud_prod: crud.Product = Depends(), crud_shoes: crud.Shoes = Depends()):
    product = crud_prod.get(prod_id)
    if product.type == 'shoes':
        product.shoes = crud_shoes.get(prod_id)
    return product



@router.put('/{prod_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Product)
def update(prod_id: int, request: schemas.BaseProduct, crud_prod: crud.Product = Depends()):
    return crud_prod.update(prod_id, request)


@router.delete('/{prod_id}')
def delete(prod_id: int, crud_prod: crud.Product = Depends(), crud_shoes: crud.Shoes = Depends()):
    product: schemas.Product = crud_prod.get(prod_id)
    if product.type == 'shoes':
        if crud_shoes.is_id_exist(prod_id):
            crud_shoes.delete(prod_id)
    crud_prod.delete(prod_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
