from typing import Generic, TypeVar
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import database

from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    table = None
    search_columns = []
    keys = ['id']
    autoincrement = True

    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create(self, request: CreateSchemaType) -> ModelType:
        if not self.autoincrement:
            keys = [getattr(request, key) for key in self.keys]
            if self._check(*keys):
                dict_keys = dict(zip(self.keys, keys))
                key_m = ', '.join([f'\'{key}\':\'{value}\'' for key, value in dict_keys.items()])
                err_mes = f'{self.table.__name__} with the {key_m} already available'
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mes)
        db_obj = self.table(**request.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create_many(self, sale_line_items: list[CreateSchemaType]) -> list[ModelType]:
        operations = [self.table(**sale_line_item.dict()) for sale_line_item in sale_line_items]
        self.db.add_all(operations)
        self.db.commit()
        return operations

    def is_id_exist(self, base_id: int):
        return self.db.query(self.table).filter(self.table.id == base_id).first()

    def _check(self, *keys):
        dict_keys = dict(zip(self.keys, keys))
        filter_table = [getattr(self.table, key) == value for key, value in dict_keys.items()]
        db_obj = self.db.query(self.table).filter(*filter_table)
        if db_obj.first():
            return True
        return False

    def _get(self, *keys):
        dict_keys = dict(zip(self.keys, keys))
        filter_table = [getattr(self.table, key) == value for key, value in dict_keys.items()]
        db_obj = self.db.query(self.table).filter(*filter_table)
        if not db_obj.first():
            key_m = ', '.join([f'\'{key}\':\'{value}\'' for key, value in dict_keys.items()])
            err_mes = f'{self.table.__name__} with the {key_m} not available'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_mes)
        return db_obj

    def get(self, *keys) -> ModelType:
        return self._get(*keys).first()

    def get_all(self, skip: int = 0, limit: int = None, q_search: str = None) -> list[ModelType]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table)

        if self.search_columns and q_search:
            search = []
            for column in self.search_columns:
                search.append(getattr(self.table, column).ilike(f'%{q_search}%'))
            db_obj = db_obj.filter(or_(*search))
        return db_obj[SLICE]

    def update(self, request: UpdateSchemaType) -> ModelType:
        db_obj = self._get(*[getattr(request, key) for key in self.keys])
        db_obj.update(request.dict())
        self.db.commit()
        return db_obj.first()

    def delete(self, *keys):
        db_obj = self._get(*keys)
        db_obj.delete(synchronize_session=False)
        self.db.commit()
