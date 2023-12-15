import os
import shutil
from urllib.parse import urlparse

import cv2
import numpy as np
import torch
from fastapi import HTTPException
from segment_anything import SamPredictor, sam_model_registry

from configs import TEMP_DIR
from configs.cos import COS_ENDPOINT
from configs.sam import SAM_MODEL_CHECKPOINT, SAM_MODEL_TYPE
from services.cos import upload_object
from utils.file import download_file
from utils.log import logger

sam = sam_model_registry[SAM_MODEL_TYPE](checkpoint=SAM_MODEL_CHECKPOINT)

if torch.cuda.is_available():
    logger.info('use cuda')
    sam.to(device=torch.device('cuda'))

predictor = SamPredictor(sam)


async def embedding_image_and_upload(url: str, uuid: str) -> str:
    """
    图片embedding
    """
    filename = urlparse(url).path.split('/')[-1]
    logger.debug(f'start get image embedding: {filename}')
    temp_dir = f'{TEMP_DIR}/{uuid}'
    os.makedirs(temp_dir, exist_ok=True)
    try:
        out_file_path = download_file(url, f'{temp_dir}/{filename}')
    except Exception as e:
        logger.error(f'download file error: {e}')
        raise HTTPException(status_code=400, detail='下载原始文件失败')

    decoded_image = cv2.imread(out_file_path)
    predictor.set_image(decoded_image)
    image_embedding_file_name = f'{temp_dir}/embedding.npy'
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(image_embedding_file_name, image_embedding)
    logger.debug(f'end get image embedding: {filename}')

    embedding_cos_file_name = f'sam/embeddings/{uuid}.npy'
    logger.debug(f'start upload image embedding: {filename}')
    upload_object(embedding_cos_file_name, image_embedding_file_name)
    logger.debug(f'end upload image embedding: {filename}')
    # 移除临时文件
    shutil.rmtree(temp_dir)
    return f'{COS_ENDPOINT}/{embedding_cos_file_name}'
