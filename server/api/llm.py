from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.llm_service import LLMService
from services.dictionary import DictionaryService
from models.llm_response import LLMExplanation


# 创建路由
router = APIRouter(prefix="/api", tags=["LLM"])

# 初始化服务（延迟初始化，避免启动时检查环境变量）
llm_service: Optional[LLMService] = None
dict_service = DictionaryService()


def get_llm_service() -> LLMService:
    """获取 LLM 服务实例（懒加载）"""
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service


class LLMExplainRequest(BaseModel):
    """LLM 解释请求"""
    word: str
    include_basic_definition: bool = True  # 是否包含本地词典的基础释义


@router.post("/llm-explain", response_model=LLMExplanation)
async def explain_word_with_llm(request: LLMExplainRequest):
    """
    使用 LLM 生成详细的单词解释

    此接口会：
    1. （可选）先从本地词典查询基础释义
    2. 调用 OpenAI API 生成详细解释
    3. 返回包含词源、例句、搭配等丰富信息的解释

    需要配置环境变量：
    - OPENAI_API_KEY: OpenAI API 密钥
    - OPENAI_BASE_URL: （可选）自定义 API 基础 URL
    - OPENAI_MODEL: （可选）使用的模型，默认 gpt-4o-mini

    参数：
    - word: 要查询的英文单词
    - include_basic_definition: 是否先查询本地词典（默认 true）

    返回：
    - LLMExplanation: 详细的单词解释
    """
    word = request.word.strip()

    if not word:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    try:
        # 获取 LLM 服务
        llm = get_llm_service()

        # 如果需要，先查询本地词典
        basic_definition = None
        if request.include_basic_definition:
            try:
                local_result = await dict_service.get_definition(word)
                # 提取中文释义作为参考
                if local_result.chinese:
                    basic_definition = local_result.chinese
            except ValueError:
                # 本地词典没有该词，继续使用 LLM
                pass

        # 调用 LLM 生成详细解释
        explanation = await llm.explain_word(word, basic_definition)

        return explanation

    except ValueError as e:
        # LLM 服务初始化失败或调用失败
        error_msg = str(e)
        if "OPENAI_API_KEY" in error_msg:
            raise HTTPException(
                status_code=503,
                detail="LLM service not configured. Please set OPENAI_API_KEY."
            )
        else:
            raise HTTPException(status_code=500, detail=error_msg)

    except Exception as e:
        print(f"Unexpected error in LLM explain: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )


@router.get("/llm-explain/{word}", response_model=LLMExplanation)
async def explain_word_with_llm_get(word: str):
    """
    使用 LLM 生成详细的单词解释（GET 方法）

    简化版接口，直接通过 URL 路径传递单词

    参数：
    - word: 要查询的英文单词

    返回：
    - LLMExplanation: 详细的单词解释
    """
    request = LLMExplainRequest(word=word, include_basic_definition=True)
    return await explain_word_with_llm(request)
