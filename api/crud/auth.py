from fastapi import status, HTTPException
from .. import tables, token
from ..schemas import user as schemas
from ..hashing import Hash
from .base import CRUDBase


class Auth(CRUDBase):
    def login(self, request: schemas.Login):
        user: tables.User = self.db.query(tables.User).filter(tables.User.email == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with the email \'{request.username}\' is not available')
        if not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Incorrect password')
        access_token = token.create_access_token(data={"sub": user.email})
        return {"access_token": access_token}
