from fastapi import APIRouter, Depends, status, Response

from .. import crud
from .. schemas import blog as schemas
from ..auth2 import get_current_user

router = APIRouter(tags=['Blogs'], prefix='/blog', dependencies=[Depends(get_current_user)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Blog)
def create(request: schemas.CreateBlog, user_id: int, crud_blog: crud.Blog = Depends()):
    return crud_blog.create_blog(request, user_id)


@router.get('/', response_model=list[schemas.Blog])
def get_all(crud_blog: crud.Blog = Depends()):
    return crud_blog.get_all()


@router.get('/{blog_id}', status_code=200, response_model=schemas.ShowBlogWithCreator)
def show(blog_id: int, crud_blog: crud.Blog = Depends()):
    return crud_blog.get(blog_id)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Blog)
def update(blog_id: int, request: schemas.UpdateBlog, crud_blog: crud.Blog = Depends()):
    return crud_blog.update(blog_id, request)


@router.delete('/{blog_id}')
def delete(blog_id: int, crud_blog: crud.Blog = Depends()):
    crud_blog.delete(blog_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
