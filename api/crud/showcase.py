import ftplib
from fastapi import UploadFile

from .. import tables
from ..schemas import showcase as schemas
from .base import CRUDBase
from ..schemas.showcase import DelImgShowcase
from ..settings import settings
from ..utilites import directory_exists, save_files, del_dir


class Showcase(CRUDBase[tables.Showcase, schemas.CreateShowcase, schemas.BaseShowcase]):
    table = tables.Showcase
    keys = ['name', 'color']
    autoincrement = False

    @staticmethod
    def del_dir_showcase(directory: str):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        del_dir(directory, ftp)
        ftp.quit()

    @staticmethod
    def save_images(directory: str, files: list[UploadFile]):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        save_files(directory, files, ftp)
        ftp.quit()

    @staticmethod
    def get_dir() -> list[schemas.ShowcaseDirs]:
        showcase_dirs: list[schemas.ShowcaseDirs] = []
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        all_files: list[str] = ftp.nlst()
        dirs = [file for file in all_files if (directory_exists(file, ftp))]
        for directory in dirs:
            ftp.cwd(directory)
            files = ftp.nlst()
            ftp.cwd('/')
            showcase_dirs.append(schemas.ShowcaseDirs(name=directory, images=files))
        ftp.quit()
        return showcase_dirs

    @staticmethod
    def del_img(request: DelImgShowcase):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        if directory_exists(request.dirName, ftp):
            ftp.cwd(request.dirName)
            ftp.delete(request.imgName)
        ftp.quit()
        return request.nameItem
