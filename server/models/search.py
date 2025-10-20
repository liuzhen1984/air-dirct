from pydantic import BaseModel
from typing import Optional, List


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str


class SimpleMeaning(BaseModel):
    """简化的词义"""
    pos: str  # 词性
    meaning: str  # 中文释义


class EnglishResult(BaseModel):
    """英文单词查询结果"""
    word: str
    phonetic: Optional[str] = None
    meanings: List[SimpleMeaning]


class ChineseResult(BaseModel):
    """中文翻译结果"""
    translations: List[str]  # 翻译结果列表


class SearchResponse(BaseModel):
    """搜索响应"""
    query: str
    is_chinese: bool
    english_result: Optional[EnglishResult] = None
    chinese_result: Optional[ChineseResult] = None
