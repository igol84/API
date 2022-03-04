from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_product_price_editor as schemas

router = APIRouter(tags=['HandlerProductPriceEditor'], prefix='/handler_product_price_editor',
                   dependencies=[Depends(get_current_user)])


@router.put('/edit_product', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ModelProduct)
def edit_product(request: schemas.ModelProduct, crud_handler: crud.HandlerProductPriceEditor = Depends()):
    return crud_handler.edit_product(request)
