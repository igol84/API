from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import seller as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Sellers'], prefix='/seller', dependencies=[Depends(allow_create_resource)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Seller)
def create(request: schemas.CreateSeller, crud_seller: crud.Seller = Depends()):
    return crud_seller.create(request)


@router.get('/', response_model=list[schemas.Seller])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_seller: crud.Seller = Depends()):
    return crud_seller.get_all(skip, limit, search)


@router.get('/{seller_id}', status_code=200, response_model=schemas.Seller)
def show(seller_id: int, crud_seller: crud.Seller = Depends()):
    return crud_seller.get(seller_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Seller)
def update(request: schemas.UpdateSeller, crud_seller: crud.Seller = Depends()):
    return crud_seller.update(request)


@router.delete('/{seller_id}')
def delete(seller_id: int, crud_seller: crud.Seller = Depends()):
    crud_seller.delete(seller_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
