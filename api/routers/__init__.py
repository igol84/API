from fastapi import APIRouter

from .user import router as user_router
from .auth import router as auth_router
from .product import router as prod_router
from .shoes import router as shoes_router
from .item import router as item_router
from .seller import router as seller_router
from .place import router as place_router
from .sale_line_item import router as sale_line_item_router
from .sale import router as sale_router
from .store import router as store_router
from .product_catalog import router as product_catalog_router
from .handler_sale_registration import router as header_sale_registration_router
from .handler_receiving_the_items import router as header_receiving_the_items

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(prod_router)
router.include_router(shoes_router)
router.include_router(product_catalog_router)
router.include_router(item_router)
router.include_router(seller_router)
router.include_router(place_router)
router.include_router(sale_line_item_router)
router.include_router(sale_router)
router.include_router(store_router)
router.include_router(header_sale_registration_router)
router.include_router(header_receiving_the_items)
