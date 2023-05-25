import ftplib

from .. import tables
from ..schemas import showcase as schemas
from .base import CRUDBase
from ..settings import settings
from ..utilites import directory_exists


class Showcase(CRUDBase[tables.Showcase, schemas.CreateShowcase, schemas.BaseShowcase]):
    table = tables.Showcase
    keys = ['name']
    autoincrement = False

    @staticmethod
    def get_dir() -> list[schemas.ShowcaseDirs]:
        showcase_dirs: list[schemas.ShowcaseDirs] = []
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_user, settings.ftp_pass)
        all_files: list[str] = ftp.nlst()
        dirs = [file for file in all_files if (directory_exists(file, ftp))]
        for dir in dirs:
            ftp.cwd(dir)
            files = ftp.nlst()
            ftp.cwd('/')
            showcase_dirs.append(schemas.ShowcaseDirs(name=dir, images=files))
        ftp.quit()
        return showcase_dirs
