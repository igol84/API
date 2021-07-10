from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import crud
from ..schemas import user as schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), crud_login: crud.Auth = Depends()):
    return crud_login.login(request)
