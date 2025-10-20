from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FavoriteCreate(BaseModel):
    """创建收藏的请求"""
    word: str
    phonetic: Optional[str] = None
    chinese: Optional[str] = None


class Favorite(BaseModel):
    """收藏记录"""
    id: str
    word: str
    phonetic: Optional[str] = None
    chinese: Optional[str] = None
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
