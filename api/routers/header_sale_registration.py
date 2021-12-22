from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import header_sale_registration as schemas

router = APIRouter(tags=['HeaderSaleRegistration'], prefix='/header_sale_registration',
                   dependencies=[Depends(get_current_user)])


@router.put('/edit_sli_price', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.SaleLineItem)
def edit_sale_price(request: schemas.EditSLIPrice, sale_line_item: crud.HeaderSaleRegistration = Depends()):
    return sale_line_item.edit_sli_price(request)
