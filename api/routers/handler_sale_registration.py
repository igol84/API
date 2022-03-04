from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_sale_registration as schemas

router = APIRouter(tags=['HandlerSaleRegistration'], prefix='/handler_sale_registration',
                   dependencies=[Depends(get_current_user)])


@router.put('/edit_sli_price', status_code=status.HTTP_202_ACCEPTED)
def edit_sale_price(request: schemas.EditSLIPrice, handler_sale_registration: crud.HeaderSaleRegistration = Depends()):
    handler_sale_registration.edit_sli_price(request)


@router.put('/put_item_from_old_sale', status_code=status.HTTP_202_ACCEPTED)
def put_item_to_old_sale(request: schemas.PutItemToOldSale, handler: crud.HeaderSaleRegistration = Depends()):
    handler.put_items_from_old_sale(request)
