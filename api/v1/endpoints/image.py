from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from schemas.image import ImageEmbeddingResponse
from services.sam import embedding_image_and_upload

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', response_model=ImageEmbeddingResponse, summary="创建图片的embedding")
async def get_image_embedding(image: Annotated[UploadFile, File(description="需要处理的图片文件")]):
    result = await embedding_image_and_upload(image)
    return result
