from typing import Generic, TypeVar

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import database

from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    table = None

    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create(self, request: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(request)
        db_obj = self.table(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def _get(self, base_id: int):
        db_obj = self.db.query(self.table).filter(self.table.id == base_id)
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} with the id \'{base_id}\' is not available')
        return db_obj

    def get(self, base_id: int) -> ModelType:
        return self._get(base_id).first()

    def get_all(self) -> list[ModelType]:
        db_obj = self.db.query(self.table).all()
        return db_obj

    def update(self, base_id: int, request: UpdateSchemaType) -> ModelType:
        db_obj = self._get(base_id)
        db_obj.update(request.dict())
        self.db.commit()
        return db_obj.first()

    def delete(self, base_id: int):
        db_obj = self._get(base_id)
        db_obj.delete(synchronize_session=False)
        self.db.commit()
