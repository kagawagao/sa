from pydantic import BaseModel, Field


class ImageEmbeddingResponse(BaseModel):
    """
    图片embedding响应
    """
    image: str = Field(..., description="图片文件地址")
    embedding: str = Field(..., description="embedding 文件地址")
