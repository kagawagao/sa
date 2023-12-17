from uuid import uuid4

from fastapi import APIRouter

from schemas.image import ImageEmbeddingReq, ImageEmbeddingResponse
from services.sam import embedding_image_and_upload

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', response_model=ImageEmbeddingResponse, summary="创建图片的embedding")
async def get_image_embedding(body: ImageEmbeddingReq):
    uuid = body.uuid if body.uuid else uuid4().hex
    embedding = await embedding_image_and_upload(url=body.image, uuid=uuid)
    return ImageEmbeddingResponse(embedding=embedding)
