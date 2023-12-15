from uuid import uuid4

from pydantic import BaseModel, Field


class ImageEmbeddingReq(BaseModel):
    """
    图片embedding请求
    """
    image: str = Field(..., description="图片文件地址")
    uuid: str = Field(..., default_factory=uuid4,
                      description="唯一标识，如果不传则自动生成")


class ImageEmbeddingResponse(BaseModel):
    """
    图片embedding响应
    """
    embedding: str = Field(..., description="embedding 文件地址")
