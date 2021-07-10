from fastapi import APIRouter, Depends
from .. import crud
from ..auth2 import get_current_user
from ..schemas import user as schemas

router = APIRouter(tags=['Users'], prefix='/user')


@router.post('/', response_model=schemas.User)
def create_user(request: schemas.CreateUser, crud_user: crud.User = Depends()):
    return crud_user.create_user(request)


@router.get('/{user_id}', response_model=schemas.UserWithBlogs)
def get_user(user_id: int, crud_user: crud.User = Depends()):
    return crud_user.get(user_id)
