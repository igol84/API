import ftplib
import json
from fastapi.encoders import jsonable_encoder
from .. import tables
from ..schemas import brand as schemas
from ..settings import settings
from .base import CRUDBase


class Brand(CRUDBase[tables.Brand, schemas.CreateBrand, schemas.BaseBrand]):
    table = tables.Brand

    def delete(self, del_brand_id: int):
        brand = self._get(del_brand_id)
        brand.delete(synchronize_session=False)
        showcase = self.db.query(tables.Showcase).filter(tables.Showcase.brand_id == del_brand_id)
        showcase.update({'brand_id': None})
        self.db.commit()

    def save_json(self):
        brands = self.get_all()
        result = jsonable_encoder(brands)

        with open("brands.json", "w", encoding='utf8') as file:
            json.dump(result, file, ensure_ascii=False)
        with open('brands.json', 'rb') as openfile:
            print(openfile)
            ftp = ftplib.FTP(settings.ftp_host, settings.ftp_xml_user, settings.ftp_xml_pass)
            ftp.storbinary('STOR ' + 'brands.json', openfile)
            ftp.quit()
        return brands


    @staticmethod
    def get_images() -> list[str]:
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_brands_user, settings.ftp_brands_pass)
        images: list[str] = ftp.nlst()
        ftp.quit()
        return images

    @staticmethod
    def save_img(file: bytes, file_name: str):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_brands_user, settings.ftp_brands_pass)
        ftp.storbinary('STOR ' + file_name, file)
        ftp.quit()

    @staticmethod
    def del_img(file_name: str):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_brands_user, settings.ftp_brands_pass)
        if file_name in ftp.nlst():
            ftp.delete(file_name)
        ftp.quit()
        return file_name
