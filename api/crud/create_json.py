import ftplib
import json
from ..settings import settings

from fastapi import Depends
from sqlalchemy.orm import Session
from .. import database
from .. import tables
from ..schemas.create_json import All, Brand, Product, Size
from ..schemas import brand as brand_schemas, showcase as showcase_schemas, product as product_schemas

PRICE_RATE = 1.4
IMG_URL_PREFIX = 'https://mirobuvi.com.ua/ftp_products'
MISSING_IMAGES = ['01', '02', '11', '12', '21', '22', '31', '32']
PREPAY = 120


class CreateJson:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def create_json(self):
        brands: list[Brand] = []
        brands_db = self.db.query(tables.Brand).all()
        for brand_db in brands_db:
            brand = brand_schemas.Brand(**brand_db.__dict__)
            brands.append(dict(brand))

        showcase_db = self.db.query(tables.Showcase).all()
        products: list[Product] = []
        for index, showcase_item_db in enumerate(showcase_db):
            showcase_item = showcase_schemas.Showcase(**showcase_item_db.__dict__)
            key = showcase_item.key
            products_db = self.db.query(tables.Product).filter(tables.Product.name == showcase_item.name).all()
            sizes: list[Size] = []
            product_type= ''
            product_url = showcase_item.url
            desc = showcase_item.desc
            desc_ua = showcase_item.desc_ua
            price = 0
            qty = None
            for product_db in products_db:
                product = product_schemas.Product(**product_db.__dict__)
                product.shoes = product_schemas.Shoes(**product_db.shoes.__dict__) if product_db.shoes else None
                product_type = product.type
                price = product.price

                if product.shoes and product.shoes.color == showcase_item.color:
                    items_db = self.db.query(tables.Item).filter(tables.Item.prod_id == product.id).all()
                    size_qty = sum([item_db.qty for item_db in items_db])
                    if size_qty:
                        size = Size(size=product.shoes.size, length=product.shoes.length, price=product.price,
                                    qty=size_qty)
                        sizes.append(size)
                elif not product.shoes:
                    items_db = self.db.query(tables.Item).filter(tables.Item.prod_id == product.id).all()
                    qty = sum([item_db.qty for item_db in items_db])
            sizes.sort(key=lambda size: size.size)
            name = f'{showcase_item.title}.'
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

            if (product_type == 'shoes' and sizes) or product_type != 'shoes':
                products.append(Product(
                    id=index + 100, type=product_type, name=name, name_ua=name_ua, brand_id=showcase_item.brand_id,
                    price=price, images=images, brand=brand, sizes=sizes, desc=desc, desc_ua=desc_ua,
                    youtube=showcase_item.youtube, qty=qty, url=product_url, product_key=key
                ))

        all: All = All(brands=brands, products=products)

        with open("data.json", "w", encoding='utf8') as file:
            json.dump(all.to_dict(), file, ensure_ascii=False, indent=2)
        with open('data.json', 'rb') as openfile:
            ftp = ftplib.FTP(settings.ftp_host, settings.ftp_xml_user, settings.ftp_xml_pass)
            ftp.storbinary('STOR ' + 'data.json', openfile)
            ftp.quit()
        return all
