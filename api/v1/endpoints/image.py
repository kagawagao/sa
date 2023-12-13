from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, File, Query, UploadFile

from schemas.image import ImageEmbeddingResponse
from services.sam import embedding_image_and_upload
from utils.log import logger

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', response_model=ImageEmbeddingResponse, summary="创建图片的embedding")
async def get_image_embedding(image: Annotated[UploadFile, File(description="需要处理的图片文件")],
                              uuid: Annotated[str, Query(..., default_factory=uuid4, description="图片的唯一标识，如果不传则自动生成")]):
    logger.debug(f'get image embedding: {image.filename}, uuid: {uuid}')
    result = await embedding_image_and_upload(image=image, uuid=uuid)
    return result
