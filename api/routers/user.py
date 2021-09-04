from fastapi import APIRouter, Depends
from .. import crud
from ..auth2 import RoleChecker
from ..schemas import user as schemas

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Users'], prefix='/user', dependencies=[Depends(allow_create_resource)])


@router.post('/', response_model=schemas.User)
def create_user(request: schemas.CreateUser, crud_user: crud.User = Depends()):
    return crud_user.create_user(request)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, crud_user: crud.User = Depends()):
    return crud_user.get(user_id)
