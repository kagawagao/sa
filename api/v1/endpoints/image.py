import asyncio
import concurrent.futures
import os
from shutil import rmtree
from tempfile import TemporaryFile
from typing import Annotated
from uuid import uuid4

import aiofiles
import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile

from configs import TEMP_DIR
from configs.cos import COS_ENDPOINT
from schemas.image import ImageEmbeddingResponse
from services.cos import upload_object
from services.sam import predictor
from utils.log import logger

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/embedding', response_model=ImageEmbeddingResponse, description="创建图片的embedding")
async def get_image_embedding(image: Annotated[UploadFile, File(description="需要处理的图片文件")]):
    logger.info(f'start get image embedding: {image.filename}')
    uuid = uuid4()
    temp_dir = f'{TEMP_DIR}/{uuid}'
    os.makedirs(temp_dir, exist_ok=True)
    out_file_path = f'{temp_dir}/{image.filename}'
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await image.read()  # async read
        await out_file.write(content)
    decoded_image = cv2.imread(out_file_path)
    predictor.set_image(decoded_image)
    image_embedding_file_name = f'{temp_dir}/embedding.npy'
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(image_embedding_file_name, image_embedding)
    logger.info(f'end get image embedding: {image.filename}')

    logger.info(f'start upload image embedding: {image.filename}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            upload_object, f'{uuid}/embedding.npy', image_embedding_file_name)
        executor.submit(
            upload_object, f'{uuid}/{image.filename}', out_file_path)

    logger.info(f'end upload image embedding: {image.filename}')
    # 移除临时文件
    rmtree(temp_dir)
    return ImageEmbeddingResponse(
        image=f'{COS_ENDPOINT}/{uuid}/{image.filename}',
        embedding=f'{COS_ENDPOINT}/{uuid}/embedding.npy'
    )


@router.post('/mask', description="创建图片蒙版")
async def create_image_mask():
    pass
