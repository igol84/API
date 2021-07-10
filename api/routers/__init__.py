from fastapi import APIRouter

from .blog import router as blog_router
from .user import router as user_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(blog_router)
