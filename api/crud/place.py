from fastapi import HTTPException
from starlette import status

from .. import tables
from ..schemas import place as schemas
from .base import CRUDBase


class Place(CRUDBase[tables.Place, schemas.CreatePlace, schemas.BasePlace]):
    table = tables.Place

    def get_all(self, skip: int = 0, limit: int = None, store_id: int = None) -> list[table]:
        if limit:
            if skip:
                SLICE = slice(skip, skip + limit)
            else:
                SLICE = slice(skip, limit)
        else:
            SLICE = slice(skip, None)
        db_obj = self.db.query(self.table)
        if store_id:
            db_obj = db_obj.where(self.table.store_id == store_id)

        return db_obj[SLICE]

    def get_by_store_id(self, store_id: int, skip: int = 0, limit: int = None) -> list[tables.Place]:
        EVEN = slice(skip, skip + limit) if limit else slice(skip, None)
        db_obj = self.db.query(self.table).where(self.table.store_id == store_id)
        if not db_obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.table.__name__} not contain \'{store_id}\' store_id')
        return db_obj[EVEN]

    def edit_name(self, data: schemas.EditPlaceName):
        place = self.db.query(tables.Place).filter(tables.Place.id == data.place_id)
        place_row = place.first()
        edited = False
        if place_row.name != data.new_name:
            edited = True
            place.update({'name': data.new_name})
        if edited:
            self.db.commit()
        return place_row

    def edit_active(self, data: schemas.EditPlaceActive):
        place = self.db.query(tables.Place).filter(tables.Place.id == data.place_id)
        place_row = place.first()
        edited = False
        if place_row.active != data.active:
            edited = True
            place.update({'active': data.active})
        if edited:
            self.db.commit()
        return place_row

    def get_all_deletable(self, store_id: int) -> list[schemas.PlaceWithDeletable]:
        places_rows = self.db.query(self.table).filter(self.table.store_id == store_id).order_by(self.table.id)
        places: list[schemas.PlaceWithDeletable] = []
        for place_row in places_rows:
            sales = self.db.query(tables.Sale).filter(tables.Sale.place_id == place_row.id).all()
            expenses = self.db.query(tables.Expense).filter(tables.Expense.place_id == place_row.id).all()
            place = schemas.PlaceWithDeletable(
                id=place_row.id, store_id=place_row.store_id, name=place_row.name, active=place_row.active,
                sales=len(sales), expenses=len(expenses))
            places.append(place)
        return places
