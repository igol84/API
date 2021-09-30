from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import product_catalog as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['ProductCatalogs'], prefix='/product_catalog', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProductCatalog)
def create(request: schemas.CreateProductCatalog, product_catalog: crud.ProductCatalog = Depends()):
    return product_catalog.create(request)


@router.get('/', response_model=list[schemas.ShowProductCatalogWithProduct])
def get_all(skip: int = None, limit: int = None, search: str = None, sli: crud.ProductCatalog = Depends()):
    return sli.get_all(skip, limit, search)


@router.get('/{store_id}/{prod_id}', status_code=200, response_model=schemas.ShowProductCatalogWithProduct)
def show(store_id: int, prod_id: int, crud_product_catalog: crud.ProductCatalog = Depends()):
    return crud_product_catalog.get_product_catalog(store_id, prod_id)


@router.put('/{store_id}/{prod_id}', status_code=status.HTTP_202_ACCEPTED,
            response_model=schemas.ProductCatalog)
def update(sale_id: int, item_id: int, sale_price: float,
           request: schemas.BaseModel, product_catalog: crud.ProductCatalog = Depends()):
    return product_catalog.update_product_catalog(sale_id, item_id, sale_price, request)


@router.delete('/{store_id}/{prod_id}')
def delete(store_id: int, prod_id: int, product_catalog: crud.ProductCatalog = Depends()):
    product_catalog.delete_product_catalog(store_id, prod_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
