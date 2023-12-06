from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from configs.cos import COS_ENDPOINT
from schemas.image import ImageEmbeddingResponse
from services.sam import embedding_image_and_upload

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', response_model=ImageEmbeddingResponse, summary="创建图片的embedding")
async def get_image_embedding(image: Annotated[UploadFile, File(description="需要处理的图片文件")]):
    image_key, embedding_key = await embedding_image_and_upload(image)
    return ImageEmbeddingResponse(
        image=f'{COS_ENDPOINT}/{image_key}',
        embedding=f'{COS_ENDPOINT}/{embedding_key}'
    )


@router.post('/mask', description="创建图片蒙版")
async def create_image_mask():
    pass
