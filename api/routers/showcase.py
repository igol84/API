from fastapi import APIRouter, Depends, status, Response, UploadFile

from .. import crud
from ..schemas import showcase as schemas
from ..auth2 import get_current_user
from ..utilites import save_file

router = APIRouter(tags=['Showcase'], prefix='/showcase', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Showcase)
def create(request: schemas.CreateShowcase, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.create(request)


@router.get('/', response_model=list[schemas.Showcase])
def get_all(skip: int = None, limit: int = None, search: str = None, crud_showcase: crud.Showcase = Depends()):
    return crud_showcase.get_all(skip, limit, search)


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
def create_file(directory: str, file: UploadFile):
    save_file(directory=directory, file_name=file.filename, file=file.file)
    return {"file_size": file.filename}
