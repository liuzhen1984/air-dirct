from pydantic import BaseModel
from typing import Optional, List


class LLMExample(BaseModel):
    """LLM 生成的例句"""
    sentence: str
    translation: str


class LLMExplanation(BaseModel):
    """LLM 增强的单词解释"""
    word: str
    pronunciation: Optional[str] = None

    # 基础释义
    basic_translation: str
    detailed_explanation: str

    # 词源和记忆
    etymology: Optional[str] = None
    memory_tips: Optional[str] = None

    # 用法说明
    usage_notes: Optional[str] = None
    common_collocations: Optional[List[str]] = None

    # 例句
    examples: List[LLMExample]

    # 相关词汇
    synonyms: Optional[List[str]] = None
    antonyms: Optional[List[str]] = None
    related_words: Optional[List[str]] = None

    # 额外信息
    difficulty_level: Optional[str] = None  # beginner/intermediate/advanced
    frequency: Optional[str] = None  # common/uncommon/rare
