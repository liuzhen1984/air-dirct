import re
from deep_translator import GoogleTranslator
from typing import List
from models.word import Meaning, Definition


class TranslationService:
    """翻译服务 - 使用 deep-translator (Google Translate)"""

    def __init__(self):
        # deep-translator uses Google Translate but is more reliable
        pass

    def detect_language(self, text: str) -> str:
        """
        检测文本语言

        Args:
            text: 待检测文本

        Returns:
            str: 语言代码 (en, zh-CN, ja, etc.)
        """
        # 检测中文
        if re.search(r'[\u4e00-\u9fa5]', text):
            return 'zh-CN'

        # 检测日文
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            return 'ja'

        # 检测韩文
        if re.search(r'[\uac00-\ud7af]', text):
            return 'ko'

        # 默认英文
        return 'en'

    async def translate(self, text: str, src: str = 'auto', dest: str = 'en') -> str:
        """
        翻译文本（异步执行以避免阻塞）

        Args:
            text: 待翻译文本
            src: 源语言 (zh-CN -> zh-Hans for deep-translator)
            dest: 目标语言

        Returns:
            str: 翻译后的文本
        """
        import asyncio

        try:
            # Convert language codes for deep-translator
            source = 'auto' if src == 'auto' else self._convert_lang_code(src)
            target = self._convert_lang_code(dest)

            translator = GoogleTranslator(source=source, target=target)
            # 在线程池中执行同步翻译，避免阻塞事件循环
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, translator.translate, text)
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            # 降级：返回原文
            return text

    def _convert_lang_code(self, code: str) -> str:
        """
        转换语言代码以适配 deep-translator

        Args:
            code: 语言代码 (zh-CN, en, etc.)

        Returns:
            str: deep-translator 兼容的语言代码
        """
        mapping = {
            'zh-CN': 'zh-CN',
            'en': 'en',
            'ja': 'ja',
            'ko': 'ko',
            'auto': 'auto'
        }
        return mapping.get(code, code)

    async def translate_batch(
        self, texts: List[str], src: str = 'en', dest: str = 'zh-CN'
    ) -> List[str]:
        """
        批量翻译（并发执行以提升性能）

        Args:
            texts: 待翻译文本列表
            src: 源语言
            dest: 目标语言

        Returns:
            List[str]: 翻译后的文本列表
        """
        import asyncio

        if not texts:
            return []

        try:
            source = self._convert_lang_code(src)
            target = self._convert_lang_code(dest)

            # 并发翻译所有文本
            async def translate_single(text: str) -> str:
                try:
                    translator = GoogleTranslator(source=source, target=target)
                    # 在线程池中执行同步翻译，避免阻塞
                    loop = asyncio.get_event_loop()
                    translated = await loop.run_in_executor(
                        None, translator.translate, text
                    )
                    return translated
                except Exception as e:
                    print(f"Error translating '{text}': {e}")
                    return text  # 保留原文

            # 并发执行所有翻译
            results = await asyncio.gather(*[translate_single(text) for text in texts])
            return list(results)

        except Exception as e:
            print(f"Batch translation error: {e}")
            return texts  # 返回原文

    async def translate_meaning(
        self, meaning: Meaning, dest: str = 'zh-CN'
    ) -> Meaning:
        """
        翻译单词释义和例句

        Args:
            meaning: 单词释义对象
            dest: 目标语言

        Returns:
            Meaning: 包含翻译的释义对象
        """
        try:
            # 收集所有需要翻译的文本
            texts_to_translate = []
            indices = []

            for idx, definition in enumerate(meaning.definitions):
                texts_to_translate.append(definition.definition)
                indices.append(('definition', idx))

                if definition.example:
                    texts_to_translate.append(definition.example)
                    indices.append(('example', idx))

            # 批量翻译
            translations = await self.translate_batch(
                texts_to_translate, src='en', dest=dest
            )

            # 映射回原结构
            translated_definitions = []
            translation_idx = 0

            for definition in meaning.definitions:
                def_chinese = translations[translation_idx]
                translation_idx += 1

                example_chinese = None
                if definition.example:
                    example_chinese = translations[translation_idx]
                    translation_idx += 1

                translated_definitions.append(
                    Definition(
                        definition=definition.definition,
                        definition_chinese=def_chinese,
                        example=definition.example,
                        example_chinese=example_chinese,
                    )
                )

            return Meaning(
                part_of_speech=meaning.part_of_speech,
                definitions=translated_definitions,
            )

        except Exception as e:
            print(f"Meaning translation error: {e}")
            return meaning  # 返回原始释义
