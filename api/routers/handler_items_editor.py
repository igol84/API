from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..auth2 import get_current_user
from ..schemas import handler_items_editor as schemas

router = APIRouter(tags=['HandlerItemEditor'], prefix='/handler_items_editor',
                   dependencies=[Depends(get_current_user)])


@router.put('/edit_item', status_code=status.HTTP_201_CREATED, response_model=schemas.ItemFormEdit)
def edit_item(request: schemas.ItemFormEdit, crud_handler: crud.HandlerItemEditor = Depends()):
    return crud_handler.edit_item(request)


@router.delete('/del_item/{item_id}')
def del_item(item_id: int, crud_handler: crud.HandlerItemEditor = Depends()):
    crud_handler.del_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/get_item_sales/{item_id}', status_code=status.HTTP_202_ACCEPTED, response_model=list[schemas.SaleDetail])
def get_item_sales(item_id: int, crud_handler: crud.HandlerItemEditor = Depends()):
    return crud_handler.get_item_sales(item_id)
