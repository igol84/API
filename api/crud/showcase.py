import ftplib
from fastapi import UploadFile
from .. import tables
from ..schemas import showcase as schemas
from .base import CRUDBase
from ..settings import settings
from ..utilites import directory_exists, save_files, del_dir


class Showcase(CRUDBase[tables.Showcase, schemas.CreateShowcase, schemas.BaseShowcase]):
    table = tables.Showcase
    keys = ['key']
    autoincrement = False

    def update(self, request: schemas.BaseShowcase) -> tables.Showcase:
        db_obj = self._get(request.key)
        db_obj.update(request.dict(exclude={'images'}))
        self.db.commit()
        return db_obj.first()

    def del_dir_showcase(self, directory: str):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        del_dir(directory, ftp)
        ftp.quit()
        row = self.db.query(tables.ShowcaseImage).filter(tables.ShowcaseImage.dir == directory)
        row.delete(synchronize_session=False)
        self.db.commit()

    def save_images(self, directory: str, files: list[UploadFile]):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        save_files(directory, files, ftp)
        ftp.quit()
        image_rows = self.db.query(tables.ShowcaseImage).filter(tables.ShowcaseImage.dir == directory).all()
        files_exist = [row.image for row in image_rows]
        operations = [tables.ShowcaseImage(dir=directory, image=file.filename)
                      for file in files if file.filename not in files_exist]
        self.db.add_all(operations)
        self.db.commit()
        return True

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

    def del_img(self, request: schemas.ShowcaseImage):
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        if directory_exists(request.dir, ftp):
            ftp.cwd(request.dir)
            ftp.delete(request.image)
        ftp.quit()
        row = self.db.query(tables.ShowcaseImage).filter(
            tables.ShowcaseImage.dir == request.dir, tables.ShowcaseImage.image == request.image
        )
        row.delete(synchronize_session=False)
        self.db.commit()
        return request.image
