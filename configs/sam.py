import os

from dotenv import load_dotenv

load_dotenv()

work_dir = os.getcwd()

model_path: str = os.getenv('SAM_MODEL_CHECKPOINT', 'sam_vit_h_4b8939.pth')

# SAM 模型地址
SAM_MODEL_CHECKPOINT = model_path.startswith(
    '/') and model_path or os.path.join(work_dir, model_path)

# SAM 模型类型
SAM_MODEL_TYPE = os.getenv('SAM_MODEL_TYPE', 'vit_h')
