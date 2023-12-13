import concurrent.futures
import os
from shutil import rmtree
from uuid import UUID

import aiofiles
import cv2
import numpy as np
import torch
from fastapi import UploadFile
from segment_anything import SamPredictor, sam_model_registry

from configs import TEMP_DIR
from configs.cos import COS_ENDPOINT
from configs.sam import SAM_MODEL_CHECKPOINT, SAM_MODEL_TYPE
from schemas.image import ImageEmbeddingResponse
from services.cos import upload_object
from utils.log import logger

sam = sam_model_registry[SAM_MODEL_TYPE](checkpoint=SAM_MODEL_CHECKPOINT)

if torch.cuda.is_available():
    logger.info('use cuda')
    sam.to(device=torch.device('cuda'))

predictor = SamPredictor(sam)


async def embedding_image_and_upload(image: UploadFile, uuid: str) -> ImageEmbeddingResponse:
    """
    图片embedding
    """
    logger.debug(f'start get image embedding: {image.filename}')
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
    logger.debug(f'end get image embedding: {image.filename}')

    logger.debug(f'start upload image embedding: {image.filename}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            upload_object, f'sam/{uuid}/embedding.npy', image_embedding_file_name)
        executor.submit(
            upload_object, f'sam/{uuid}/{image.filename}', out_file_path)

    logger.debug(f'end upload image embedding: {image.filename}')
    # 移除临时文件
    rmtree(temp_dir)
    return ImageEmbeddingResponse(
        image=f'{COS_ENDPOINT}/sam/{uuid}/{image.filename}',
        embedding=f'{COS_ENDPOINT}/sam/{uuid}/embedding.npy',
        key=f'{uuid}',
        mask_key=f'sam/{uuid}/{image.filename}'
    )
