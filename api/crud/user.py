from fastapi import HTTPException
from starlette import status
from .. import tables
from ..hashing import Hash
from ..schemas import user as schemas
from .base import CRUDBase


class User(CRUDBase):

    def create_user(self, request: schemas.CreateUser) -> tables.User:
        new_user = tables.User(name=request.name, email=request.email, password=Hash.bvcrypt(request.password))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get(self, user_id: int) -> tables.User:
        user = self.db.query(tables.User).filter(tables.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with the id \'{user_id}\' is not available')
        return user
