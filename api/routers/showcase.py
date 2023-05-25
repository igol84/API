from fastapi import APIRouter, Depends, status, Response, UploadFile

from .. import crud
from ..schemas import showcase as schemas
from ..auth2 import RoleChecker
from ..utilites import save_files, del_dir

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Showcase'], prefix='/showcase', dependencies=[Depends(allow_create_resource)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Showcase)
def create(request: schemas.CreateShowcase, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.create(request)


@router.get('/', response_model=list[schemas.Showcase])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.get_all(skip, limit, search)


@router.get('/dir', response_model=list[schemas.ShowcaseDirs])
def get_dir_url(crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.get_dir()


@router.get('/{name}', status_code=200, response_model=schemas.Showcase)
def show(name: str, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.get(name)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Showcase)
def update(request: schemas.UpdateShowcase, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.update(request)


@router.delete('/{name}')
def delete(name: str, crud_showcase: crud.Showcase = Depends()):
    crud_showcase.delete(name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/files/{directory}", status_code=status.HTTP_201_CREATED)
def create_file(directory: str, files: list[UploadFile]):
    save_files(directory=directory, files=files)
    return {"file_save": 'ok'}


@router.delete("/dir/{directory}")
def delete_directory(directory: str):
    del_dir(directory=directory)
    return Response(status_code=status.HTTP_204_NO_CONTENT)