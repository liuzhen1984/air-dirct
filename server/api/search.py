from fastapi import APIRouter, HTTPException
from models.search import SearchRequest, SearchResponse, SimpleMeaning, EnglishResult, ChineseResult
from models.word import WordDefinition
from services import DictionaryService, TranslationService

router = APIRouter(prefix="/api", tags=["search"])

# 初始化服务
dict_service = DictionaryService()
trans_service = TranslationService()


@router.post("/search", response_model=SearchResponse)
async def search_word(request: SearchRequest):
    """
    简化版搜索接口
    - 输入英文 → 本地库查询，返回简单的中文释义和词性
    - 输入中文 → GoogleTranslate直接翻译，返回英文结果(可能多个)
    """
    query = request.query.strip()

    print(f"\n=== Search Request ===")
    print(f"Query: {query}")

    # 检测语言
    detected_lang = trans_service.detect_language(query)
    is_chinese = detected_lang == 'zh-CN'

    print(f"Detected language: {detected_lang}")

    if is_chinese:
        # 中文输入：直接翻译成英文
        translation = await trans_service.translate(query, src='zh-CN', dest='en')
        print(f"Chinese to English: {translation}")

        # 如果翻译结果包含多个词(用逗号或顿号分隔),拆分成列表
        translations = [t.strip() for t in translation.replace('、', ',').split(',')]

        response = SearchResponse(
            query=query,
            is_chinese=True,
            chinese_result=ChineseResult(translations=translations)
        )
    else:
        # 英文输入：从本地库查询
        try:
            definition = await dict_service.get_definition(query)

            # 提取简化的释义
            meanings = []
            for meaning in definition.meanings:
                # 合并所有定义为一个字符串
                definitions_list = []
                for def_item in meaning.definitions:
                    if def_item.definition_chinese:
                        definitions_list.append(def_item.definition_chinese)

                if definitions_list:
                    combined_meaning = '; '.join(definitions_list)
                    meanings.append(SimpleMeaning(
                        pos=meaning.part_of_speech,
                        meaning=combined_meaning
                    ))

            response = SearchResponse(
                query=query,
                is_chinese=False,
                english_result=EnglishResult(
                    word=definition.word,
                    phonetic=definition.phonetic,
                    meanings=meanings
                )
            )

        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    print(f"=== Search Complete ===\n")
    return response


@router.get("/definition/{word}", response_model=WordDefinition)
async def get_definition(word: str):
    """
    获取英文单词释义（带中文翻译）
    """
    print(f"\n=== Definition Request ===")
    print(f"Word: {word}")

    try:
        # 获取词典释义
        definition = await dict_service.get_definition(word)

        # 翻译单词为中文
        chinese_translation = await trans_service.translate(
            word, src='en', dest='zh-CN'
        )

        # 翻译所有释义
        translated_meanings = []
        for meaning in definition.meanings:
            translated_meaning = await trans_service.translate_meaning(meaning)
            translated_meanings.append(translated_meaning)

        result = WordDefinition(
            word=definition.word,
            phonetic=definition.phonetic,
            chinese=chinese_translation,
            meanings=translated_meanings,
        )

        print(f"=== Definition Complete ===\n")
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
