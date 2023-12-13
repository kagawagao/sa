from typing import Annotated

from fastapi import APIRouter, Path, Query

from services.cos import get_presigned_url
from utils.log import logger

router = APIRouter(prefix="/cos", tags=["cos"])


@router.get('/url', response_model=str, summary="获取上传地址")
async def get_upload_url_by_key(key: Annotated[str, Query(..., description="上传文件的key")]):
    logger.debug(f'get upload url by key: {key}')
    return get_presigned_url(key)
