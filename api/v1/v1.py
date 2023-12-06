from fastapi import APIRouter

from .endpoints import image_router

router = APIRouter(prefix="/v1")

router.include_router(image_router)
