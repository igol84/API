from fastapi import APIRouter, Depends, status, Response

from .. import crud
from ..schemas import tag_url as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['TagUrl'], prefix='/tag_url', dependencies=[Depends(allow_create_resource)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TagUrl)
def create(request: schemas.CreateTagUrl, crud_tag_url: crud.TagUrl = Depends()):
    return crud_tag_url.create(request)


@router.get('/', response_model=list[schemas.TagUrl])
def get_all(skip: int = None, limit: int = None, store_id: int = None, crud_tag_url: crud.TagUrl = Depends()):
    return crud_tag_url.get_all(skip, limit, store_id)


@router.get('/{tag_url}', status_code=200, response_model=schemas.TagUrl)
def show(tag_url: str, crud_tag_url: crud.TagUrl = Depends()):
    return crud_tag_url.get(tag_url)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.TagUrl)
def update(request: schemas.UpdateTagUrl, crud_tag_url: crud.TagUrl = Depends()):
    return crud_tag_url.update(request)


@router.delete('/{tag_url_id}')
def delete(tag_url: str, crud_tag_url: crud.TagUrl = Depends()):
    crud_tag_url.delete(tag_url)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
