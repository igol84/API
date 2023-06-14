import ftplib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from .. import tables

from .. import database
from ..settings import settings
from ..schemas import brand as brand_schemas, showcase as showcase_schemas, product as product_schemas

PRICE_RATE = 1.4
IMG_URL_PREFIX = 'https://mirobuvi.com.ua/ftp_products'
MISSING_IMAGES = ['01', '02', '11', '12', '21', '22', '31', '32']
PREPAY = 120


@dataclass
class Size:
    size: float
    length: str
    price: float


@dataclass
class Product:
    id: int
    type: str
    name: str
    name_ua: str
    category_id: int
    price: float
    images: list[str]
    brand: Optional[str]
    sizes: list[Size]
    desc: str
    desc_ua: str
    youtube: Optional[str]


class Xml:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create_xml(self):
        brands_db = self.db.query(tables.Brand).all()
        showcase_db = self.db.query(tables.Showcase).filter(tables.Showcase.prom_active).all()

        shop = ET.Element('shop')

        categories = ET.SubElement(shop, 'categories')
        for brand_db in brands_db:
            brand = brand_schemas.Brand(**brand_db.__dict__)
            category = ET.SubElement(categories, 'category', id=str(brand.id))
            category.text = brand.name

        products: list[Product] = []
        for index, showcase_item_db in enumerate(showcase_db):
            showcase_item = showcase_schemas.Showcase(**showcase_item_db.__dict__)
            products_db = self.db.query(tables.Product).filter(tables.Product.name == showcase_item.name).all()

            sizes: list[Size] = []
            product_type, desc, desc_ua = '', '', ''
            for product_db in products_db:
                product = product_schemas.Product(**product_db.__dict__)
                product.shoes = product_schemas.Shoes(**product_db.shoes.__dict__) if product_db.shoes else None
                product_type = product.type
                if product.shoes and product.shoes.color == showcase_item.color:
                    items_db = self.db.query(tables.Item).filter(tables.Item.prod_id == product.id).all()
                    size_qty = sum([item_db.qty for item_db in items_db])
                    if size_qty:
                        length = f'{product.shoes.length: g}см.' if product.shoes.length else ''
                        sizes.append(Size(size=product.shoes.size, length=length, price=product.price))
            max_price = max([size.price for size in sizes])
            price = round(int(max_price * PRICE_RATE), -1) + 10
            prepay = PREPAY if price > PREPAY else price
            name_sizes = ', '.join([f'{size.size: g}' for size in sizes])
            if product_type == 'shoes':
                name = f'{showcase_item.title_ua}. Размеры в наличии: {name_sizes}'
                name_ua = f'{showcase_item.title_ua}. Розміри в наявності: {name_sizes}'
                tr_sizes = ''.join([f'<tr><td>{size.size: g}</td> <td>{size.length}</td></tr>' for size in sizes])
                youtube = \
                    f'<div style="position:relative;height:0;padding-bottom:56.25%">' \
                    f'<iframe src="https://www.youtube.com/embed/{showcase_item.youtube}?ecver=2" width="640" ' \
                    f'height="360" frameborder="0" style="position:absolute;width:100%;height:100%;left:0"' \
                    f' allowfullscreen></iframe></div>' if showcase_item.youtube else ''
                desc = \
                    f'<br/><strong><span style="color: red">-Предоплата {prepay}грн</span></strong><br/> <br/>' \
                    f' -остальная стоимость и доставка оплачивается при получении на Новой Почте. Или ПромОплата' \
                    f'<br/>Доставка 1-2 дня!' \
                    f'<table border="1" style="width:500px"><tbody><tr>' \
                    f'<th>Размеры в наличии</th> <th>Длина стельки(см)</th></tr>' \
                    f'{tr_sizes}' \
                    f'</tbody></table>' \
                    f'{youtube}'
                desc_ua = \
                    f'<br/><strong><span style="color: red">-Передоплата {prepay}грн</span></strong>' \
                    f'<br/><br/> -інша вартість і доставка оплачується при отриманні на Новій Пошті. ' \
                    f'Або ПромОплата<br/>Доставка 1-2 дня!' \
                    f'<table border="1" style="width:500px"><tbody><tr>' \
                    f'<tr><th>Розміри в наявності</th> <th>Довжина устілки(см)</th> </tr>' \
                    f'{tr_sizes}' \
                    f'</tbody></table><br/>' \
                    f'{youtube}'
            else:
                name = f'{showcase_item.title_ua}.'
                name_ua = f'{showcase_item.title_ua}.'
            images_db = self.db.query(tables.ShowcaseImage).filter(tables.ShowcaseImage.dir == showcase_item.key).all()
            images: list[str] = []
            for image_db in images_db:
                img_name = image_db.image.split('.')[0]
                if img_name not in MISSING_IMAGES:
                    images.append(f'{IMG_URL_PREFIX}/{showcase_item.key}/{image_db.image}')

            brand = None
            if showcase_item.brand_id:
                brand = self.db.query(tables.Brand).filter(tables.Brand.id == showcase_item.brand_id).first().name

            if product_type == 'shoes' and sizes:
                products.append(Product(
                    id=index, type=product_type, name=name_ua, name_ua=name, category_id=showcase_item.brand_id,
                    price=price, images=images, brand=brand, sizes=sizes, desc=desc, desc_ua=desc_ua,
                    youtube=showcase_item.youtube
                ))
            else:
                products.append(Product(
                    id=index, type=product_type, name=name_ua, name_ua=name, category_id=showcase_item.brand_id,
                    price=price, images=images, brand=brand, sizes=sizes, desc=desc, desc_ua=desc_ua,
                    youtube=showcase_item.youtube
                ))

        for product in products:
            offers = ET.SubElement(shop, 'offers')
            offer = ET.SubElement(offers, 'offer', id=str(product.id), available="true", in_stock="На складі")
            name = ET.SubElement(offer, 'name')
            name.text = product.name
            name_ua = ET.SubElement(offer, 'name_ua')
            name_ua.text = product.name_ua
            categoryId = ET.SubElement(offer, 'categoryId')
            categoryId.text = str(product.category_id)
            portal_category_id = ET.SubElement(offer, 'portal_category_id')
            portal_category_id.text = '3220713'
            price = ET.SubElement(offer, 'price')
            price.text = str(product.price)
            ET.SubElement(offer, 'oldprice')
            currencyId = ET.SubElement(offer, 'currencyId')
            currencyId.text = 'UAH'
            for image in product.images:
                picture = ET.SubElement(offer, 'picture')
                picture.text = image
            if product.brand:
                vendor = ET.SubElement(offer, 'vendor')
                vendor.text = product.brand
            barcode = ET.SubElement(offer, 'barcode')
            barcode.text = str(product.id)
            description = ET.SubElement(offer, 'description')
            description.text = product.desc
            description_ua = ET.SubElement(offer, 'description_ua')
            description_ua.text = product.desc_ua

        with open('catalog.xml', 'wb') as f:
            doc_type = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">'
            to_string = ET.tostring(shop).decode('utf-8')
            created_file = f"{doc_type}{to_string}"
            f.write(bytes(created_file, 'UTF-8'))

        file = open('catalog.xml', 'rb')
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_xml_user, settings.ftp_xml_pass)
        ftp.storbinary('STOR ' + 'catalog.xml', file)
        ftp.quit()
        return created_file
