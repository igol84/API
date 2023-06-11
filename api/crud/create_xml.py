import ftplib
import xml.etree.ElementTree as ET
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import tables

from .. import database
from ..settings import settings
from ..schemas import brand as brand_schemas, showcase as showcase_schemas


class Xml:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create_xml(self):
        brands_db = self.db.query(tables.Brand).all()
        showcase_db = self.db.query(tables.Showcase).all()

        shop = ET.Element('shop')

        categories = ET.SubElement(shop, 'categories')
        for brand_db in brands_db:
            brand = brand_schemas.Brand(**brand_db.__dict__)
            category = ET.SubElement(categories, 'category', id=str(brand.id))
            category.text = brand.name

        offers = ET.SubElement(shop, 'offers')
        for index, item_db in enumerate(showcase_db):
            item = showcase_schemas.Showcase(**item_db.__dict__)
            available = "true" if item.active else "false"
            offer = ET.SubElement(offers, 'offer', id=str(index), available=available, in_stock="На складі")
            name = ET.SubElement(offer, 'name')
            name.text = item.title
            name_ua = ET.SubElement(offer, 'name_ua')
            name_ua.text = item.title_ua
            categoryId = ET.SubElement(offer, 'categoryId')
            categoryId.text = item.brand_id

        with open('catalog.xml', 'wb') as f:
            doc_type = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">'
            tostring = ET.tostring(shop).decode('utf-8')
            created_file = f"{doc_type}{tostring}"
            f.write(bytes(created_file, 'UTF-8'))

        file = open('catalog.xml', 'rb')
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_xml_user, settings.ftp_xml_pass)
        ftp.storbinary('STOR ' + 'catalog.xml', file)
        ftp.quit()
        return created_file

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
