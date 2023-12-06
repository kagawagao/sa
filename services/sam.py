import os

import cv2
import numpy as np
from fastapi import UploadFile
from segment_anything import SamPredictor, sam_model_registry

from configs.sam import SAM_MODEL_CHECKPOINT, SAM_MODEL_TYPE

sam = sam_model_registry[SAM_MODEL_TYPE](checkpoint=SAM_MODEL_CHECKPOINT)

predictor = SamPredictor(sam)
