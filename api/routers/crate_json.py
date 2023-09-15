from fastapi import APIRouter, Depends
from ..schemas import brand as schemas
from .. import crud

router = APIRouter(tags=['Crate Json'], prefix='/crate-json')  #


@router.get('')
def save_json(crud_brand: crud.CreateJson = Depends()):
    return crud_brand.create_json()