from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_product_price_editor as schemas

router = APIRouter(tags=['HandlerProductPriceEditor'], prefix='/handler_product_price_editor',
                   dependencies=[Depends(get_current_user)])

@router.put('/edit_product', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ModelProductForm)
def edit_product(request: schemas.ModelProductForm, crud_handler: crud.HandlerProductPriceEditor = Depends()):
    return crud_handler.edit_product(request)


@router.put('/edit_size', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ModelSizeForm)
def edit_size(request: schemas.ModelSizeForm, crud_handler: crud.HandlerProductPriceEditor = Depends()):
    return crud_handler.edit_size(request)


@router.put('/edit_shoes', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ModelShoesForm)
def edit_shoes(request: schemas.ModelShoesForm, crud_handler: crud.HandlerProductPriceEditor = Depends()):
    return crud_handler.edit_shoes(request)


@router.put('/edit_color', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ModelColorForm)
def edit_color(request: schemas.ModelColorForm, crud_handler: crud.HandlerProductPriceEditor = Depends()):
    return crud_handler.edit_color(request)