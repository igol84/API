from fastapi import APIRouter

from .user import router as user_router
from .auth import router as auth_router
from .product import router as prod_router
from .shoes import router as shoes_router
from .item import router as item_router
from .seller import router as seller_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(prod_router)
router.include_router(shoes_router)
router.include_router(item_router)
router.include_router(seller_router)
