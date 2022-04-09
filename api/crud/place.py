from .. import tables
from ..schemas import place as schemas
from .base import CRUDBase


class Place(CRUDBase[tables.Place, schemas.CreatePlace, schemas.BasePlace]):
    table = tables.Place

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
