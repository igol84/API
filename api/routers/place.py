from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import place as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Places'], prefix='/place', dependencies=[Depends(allow_create_resource)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Place)
def create(request: schemas.CreatePlace, crud_place: crud.Place = Depends()):
    return crud_place.create(request)


@router.get('/', response_model=list[schemas.Place])
def get_all(skip: int = None, limit: int = None, store_id: int = None, crud_place: crud.Place = Depends()):
    return crud_place.get_all(skip, limit, store_id)


@router.get('/deletable', response_model=list[schemas.PlaceWithDeletable])
def get_all_deletable(store_id: int, crud_place: crud.Place = Depends()):
    return crud_place.get_all_deletable(store_id)


@router.get('/get_by_store_id/{store_id}', response_model=list[schemas.Place])
def get_by_store_id(store_id: int, crud_place: crud.Place = Depends()):
    return crud_place.get_by_store_id(store_id)


@router.get('/{place_id}', status_code=200, response_model=schemas.Place)
def show(place_id: int, crud_place: crud.Place = Depends()):
    return crud_place.get(place_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Place)
def update(request: schemas.UpdatePlace, crud_place: crud.Place = Depends()):
    return crud_place.update(request)


@router.delete('/{place_id}')
def delete(place_id: int, crud_place: crud.Place = Depends()):
    crud_place.delete(place_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/edit_name', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Place)
def update(request: schemas.EditPlaceName, crud_place: crud.Place = Depends()):
    return crud_place.edit_name(request)


@router.put('/edit_active', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Place)
def update(request: schemas.EditPlaceActive, crud_place: crud.Place = Depends()):
    return crud_place.edit_active(request)
