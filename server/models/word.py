from pydantic import BaseModel
from typing import List, Optional


class Definition(BaseModel):
    """单个释义"""
    definition: str
    definition_chinese: Optional[str] = None
    example: Optional[str] = None
    example_chinese: Optional[str] = None


class Meaning(BaseModel):
    """词性分组的释义"""
    part_of_speech: str
    definitions: List[Definition]


class WordDefinition(BaseModel):
    """单词完整释义"""
    word: str
    phonetic: Optional[str] = None
    chinese: Optional[str] = None
    meanings: List[Meaning]
