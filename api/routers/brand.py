from fastapi import APIRouter, Depends, status, Response, UploadFile

from .. import crud
from ..schemas import brand as schemas
from ..auth2 import RoleChecker

allow_create_resource = RoleChecker(["admin"])
router = APIRouter(tags=['Brand'], prefix='/brand', dependencies=[Depends(allow_create_resource)])  #


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Brand)
def create(request: schemas.CreateBrand, crud_brand: crud.Brand = Depends()):
    return crud_brand.create(request)


@router.get('/', response_model=list[schemas.Brand])
def get_all(skip: int = None, limit: int = None, store_id: int = None, crud_brand: crud.Brand = Depends()):
    return crud_brand.get_all(skip, limit, store_id)


@router.get('/images', response_model=list[str])
def get_images(crud_brand: crud.Brand = Depends()):
    return crud_brand.get_images()


@router.post("/image/{brand_id}", status_code=status.HTTP_201_CREATED)
def create_image(brand_id: int, file: UploadFile, crud_brand: crud.Brand = Depends()):
    crud_brand.save_img(file=file.file, file_name=f'{brand_id}.jpg')
    return {"file_save": 'ok'}


@router.get('/{brand_id}', status_code=200, response_model=schemas.Brand)
def show(brand_id: int, crud_brand: crud.Brand = Depends()):
    return crud_brand.get(brand_id)


@router.put('/', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Brand)
def update(request: schemas.UpdateBrand, crud_brand: crud.Brand = Depends()):
    return crud_brand.update(request)


@router.delete('/{brand_id}')
def delete(brand_id: int, crud_brand: crud.Brand = Depends()):
    crud_brand.delete(brand_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/image/{brand_id}")
def delete_directory(brand_id: int, crud_brand: crud.Brand = Depends()):
    crud_brand.del_img(file_name=f'{brand_id}.jpg')
    return Response(status_code=status.HTTP_204_NO_CONTENT)