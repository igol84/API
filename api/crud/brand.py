import ftplib

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
