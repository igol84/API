from fastapi import APIRouter, Depends, status

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_items_editor as schemas

router = APIRouter(tags=['HandlerItemEditor'], prefix='/handler_items_editor',
                   dependencies=[Depends(get_current_user)])


@router.put('/edit_item', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ItemFormEdit)
def edit_item(request: schemas.ItemFormEdit, crud_handler: crud.HandlerItemEditor = Depends()):
    return crud_handler.edit_item(request)


@router.put('/del_item', status_code=status.HTTP_202_ACCEPTED)
def del_item(request: schemas.ItemFormDel, crud_handler: crud.HandlerItemEditor = Depends()):
    crud_handler.del_item(request)
