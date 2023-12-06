import os
from tempfile import TemporaryFile
from typing import Annotated
from uuid import uuid4

import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile

from services.cos import upload_object
from services.sam import predictor

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', description="创建图片的embedding")
async def get_image_embedding(image: Annotated[UploadFile, File(description="需要处理的图片文件")]):
    decoded_image = cv2.imdecode(np.fromstring(
        image.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    predictor.set_image(decoded_image)
    uuid = uuid4()
    image_embedding_file_name = f'{uuid}/{image.filename}_embedding.npy'
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(image_embedding_file_name, image_embedding)
    upload_object(image_embedding_file_name, image_embedding_file_name)
    upload_object(f'{uuid}/{image.filename}', image.file)
    return {"result": 'success'}


@router.post('/mask', description="创建图片蒙版")
async def create_image_mask():
    pass
