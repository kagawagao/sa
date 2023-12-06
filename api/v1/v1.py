from fastapi import APIRouter

from .endpoints import cos_router, image_router

router = APIRouter(prefix="/v1")

router.include_router(image_router)
router.include_router(cos_router)
