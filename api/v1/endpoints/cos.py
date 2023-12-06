from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from services.cos import get_presigned_url

router = APIRouter(prefix="/cos", tags=["cos"])


@router.get('/url/{key}', response_model=str, summary="获取上传地址")
async def get_upload_url_by_key(key: str):
    return get_presigned_url(key)
