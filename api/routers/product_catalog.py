from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import product_catalog as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['ProductCatalogs'], prefix='/product_catalog', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowRowProductCatalogWithProduct)
def create_row(request: schemas.CreateRowProductCatalog, product_catalog: crud.ProductCatalog = Depends()):
    return product_catalog.create(request)


@router.get('/', response_model=list[schemas.ShowRowProductCatalogWithProduct])
def get_all_rows(skip: int = None, limit: int = None, search: str = None, crud_pc: crud.ProductCatalog = Depends()):
    return crud_pc.get_all(skip, limit, search)


@router.get('/{store_id}/{prod_id}')
def check_row(store_id: int, prod_id: int, crud_product_catalog: crud.ProductCatalog = Depends()):
    if crud_product_catalog.check(store_id, prod_id):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{store_id}', status_code=200, response_model=list[schemas.ShowRowProductCatalogWithProduct])
def get_store_pc(store_id: int, skip: int = None, limit: int = None, crud_pc: crud.ProductCatalog = Depends()):
    return crud_pc.get_store_pc(store_id, skip, limit)


@router.delete('/{store_id}/{prod_id}')
def delete_row(store_id: int, prod_id: int, crud_pc: crud.ProductCatalog = Depends()):
    crud_pc.delete(store_id, prod_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
