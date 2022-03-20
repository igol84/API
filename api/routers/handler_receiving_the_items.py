from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_receiving_the_items as schemas

router = APIRouter(tags=['HandlerReceivingTheItems'], prefix='/handler_receiving_the_item',
                   dependencies=[Depends(get_current_user)])


@router.put('/receiving_the_items', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.OutputItems)
def receiving_the_items(request: schemas.ModelProduct, crud_handler: crud.HeaderReceivingTheItems = Depends()):
    return crud_handler.receiving_the_items(request)
