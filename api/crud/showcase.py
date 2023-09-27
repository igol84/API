import ftplib
from fastapi import UploadFile, HTTPException, status
from .. import tables
from ..schemas import showcase as showcase_schemas, product as product_schemas
from .base import CRUDBase
from ..settings import settings
from ..utilites import directory_exists, save_files, del_dir, check_file_name_and_get_new_name

MISSING_IMAGES = ['01', '02', '11', '12', '21', '22', '31', '32']
IMG_URL_PREFIX = 'https://mirobuvi.com.ua/ftp_products'


class Showcase(CRUDBase[tables.Showcase, showcase_schemas.CreateShowcase, showcase_schemas.BaseShowcase]):
    table = tables.Showcase
    keys = ['key']
    autoincrement = False

    def update(self, request: showcase_schemas.BaseShowcase) -> tables.Showcase:
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
        operations = [tables.ShowcaseImage(dir=directory, image=check_file_name_and_get_new_name(file.filename))
                      for file in files if file.filename not in files_exist]
        self.db.add_all(operations)
        self.db.commit()
        return True

    @staticmethod
    def get_dir() -> list[showcase_schemas.ShowcaseDirs]:
        showcase_dirs: list[showcase_schemas.ShowcaseDirs] = []
        ftp = ftplib.FTP(settings.ftp_host, settings.ftp_products_user, settings.ftp_products_pass)
        all_files: list[str] = ftp.nlst()
        dirs = [file for file in all_files if (directory_exists(file, ftp))]
        for directory in dirs:
            ftp.cwd(directory)
            files = ftp.nlst()
            ftp.cwd('/')
            showcase_dirs.append(showcase_schemas.ShowcaseDirs(name=directory, images=files))
        ftp.quit()
        return showcase_dirs

    def del_img(self, request: showcase_schemas.ShowcaseImage):
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

    def get_products_by_brand_id(self, brand_id: int) -> list[showcase_schemas.Product]:
        showcase_db = self.db.query(tables.Showcase).filter(tables.Showcase.brand_id == brand_id).all()
        products: list[showcase_schemas.Product] = []
        for index, showcase_item_db in enumerate(showcase_db):
            showcase_item = showcase_schemas.Showcase(**showcase_item_db.__dict__)
            key = showcase_item.key
            products_db = self.db.query(tables.Product).filter(tables.Product.name == showcase_item.name).all()
            sizes: list[showcase_schemas.Size] = []
            product_type = ''
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
                        size = showcase_schemas.Size(size=product.shoes.size, length=product.shoes.length,
                                                     price=product.price, qty=size_qty)
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
                products.append(showcase_schemas.Product(
                    id=key, type=product_type, name=name, name_ua=name_ua, brand_id=showcase_item.brand_id,
                    price=price, images=images, brand=brand, sizes=sizes, desc=desc, desc_ua=desc_ua,
                    youtube=showcase_item.youtube, qty=qty, url=product_url, product_key=key
                ))
        return products

    def get_product_by_url(self, product_url: str) -> showcase_schemas.Product:
        showcase_item_db = self.db.query(tables.Showcase).filter(tables.Showcase.url == product_url).first()
        if not showcase_item_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Product with the url \'{product_url}\' is not available')
        showcase_item = showcase_schemas.Showcase(**showcase_item_db.__dict__)
        key = showcase_item.key
        products_db = self.db.query(tables.Product).filter(tables.Product.name == showcase_item.name).all()
        sizes: list[showcase_schemas.Size] = []
        product_type = ''
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
                    size = showcase_schemas.Size(size=product.shoes.size, length=product.shoes.length,
                                                 price=product.price, qty=size_qty)
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
            return showcase_schemas.Product(
                id=key, type=product_type, name=name, name_ua=name_ua, brand_id=showcase_item.brand_id,
                price=price, images=images, brand=brand, sizes=sizes, desc=desc, desc_ua=desc_ua,
                youtube=showcase_item.youtube, qty=qty, url=product_url, product_key=key
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Product with the url \'{product_url}\' is not available')
