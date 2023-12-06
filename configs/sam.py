import os

from dotenv import load_dotenv

load_dotenv()

work_dir = os.getcwd()

model_path: str = os.getenv('SAM_MODEL_CHECKPOINT')

# SAM 模型地址
SAM_MODEL_CHECKPOINT = model_path.startswith(
    '/') and model_path or os.path.join(work_dir, model_path)

# SAM 模型类型
SAM_MODEL_TYPE = os.getenv('SAM_MODEL_TYPE')

# SAM embedding 临时存放目录
SAM_EMBEDDING_DIR = os.path.join(work_dir, 'embeddings')

# SAM 图片临时存放目录
SAM_IMAGE_DIR = os.path.join(work_dir, 'images')
