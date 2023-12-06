import os

import cv2
import numpy as np
from fastapi import UploadFile
from segment_anything import SamPredictor, sam_model_registry

from configs.sam import SAM_EMBEDDING_DIR, SAM_MODEL_CHECKPOINT, SAM_MODEL_TYPE

sam = sam_model_registry[SAM_MODEL_TYPE](checkpoint=SAM_MODEL_CHECKPOINT)

predictor = SamPredictor(sam)


async def create_image_embedding(file: UploadFile) -> str:
    """
    创建图片的embedding
    :param file: 图片文件
    :return: embedding
    """
    image = cv2.imdecode(np.fromstring(
        file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    return image_embedding
