import os
import json
from typing import Optional
from openai import AsyncOpenAI
from models.llm_response import LLMExplanation, LLMExample


class LLMService:
    """LLM 增强词典服务 - 使用 OpenAI API"""

    def __init__(self):
        """
        初始化 OpenAI 客户端

        需要设置环境变量:
        - OPENAI_API_KEY: OpenAI API 密钥
        - OPENAI_BASE_URL: (可选) 自定义 API 基础 URL
        - OPENAI_MODEL: (可选) 使用的模型，默认 gpt-4o-mini
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in .env file or environment."
            )

        base_url = os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # 初始化客户端
        if base_url:
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = AsyncOpenAI(api_key=api_key)

    async def explain_word(
        self,
        word: str,
        basic_definition: Optional[str] = None
    ) -> LLMExplanation:
        """
        使用 LLM 生成详细的单词解释

        Args:
            word: 要解释的英文单词
            basic_definition: 基础释义（来自本地词典），可选

        Returns:
            LLMExplanation: 详细的单词解释
        """
        # 构建 prompt
        prompt = self._build_prompt(word, basic_definition)

        try:
            # 调用 OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional English teacher and linguist. "
                            "Provide detailed, educational explanations of English words "
                            "in Chinese. Format your response as valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # 解析响应
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI API")

            data = json.loads(content)

            # 转换为 LLMExplanation 模型
            return self._parse_response(word, data)

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise ValueError(f"Failed to generate explanation: {str(e)}")

    def _build_prompt(self, word: str, basic_definition: Optional[str]) -> str:
        """构建发送给 LLM 的 prompt"""
        prompt = f"""请详细解释英文单词 "{word}"，并以 JSON 格式返回以下信息：

{{
  "basic_translation": "简明中文翻译（一句话）",
  "detailed_explanation": "详细解释（2-3句话，说明含义、用法场景）",
  "pronunciation": "音标（如果知道的话，使用 IPA 格式）",
  "etymology": "词源（单词的来源和演变，可选）",
  "memory_tips": "记忆技巧（帮助记忆的方法，可选）",
  "usage_notes": "用法说明（常见搭配、注意事项等）",
  "common_collocations": ["常见搭配1", "常见搭配2", "..."],
  "examples": [
    {{
      "sentence": "英文例句1",
      "translation": "中文翻译1"
    }},
    {{
      "sentence": "英文例句2",
      "translation": "中文翻译2"
    }},
    {{
      "sentence": "英文例句3",
      "translation": "中文翻译3"
    }}
  ],
  "synonyms": ["近义词1", "近义词2", "..."],
  "antonyms": ["反义词1", "反义词2", "..."],
  "related_words": ["相关词1", "相关词2", "..."],
  "difficulty_level": "beginner/intermediate/advanced",
  "frequency": "common/uncommon/rare"
}}
"""

        # 如果有基础释义，添加到 prompt
        if basic_definition:
            prompt += f"\n参考释义：{basic_definition}\n"

        prompt += """
要求：
1. 所有解释和翻译使用简体中文
2. 例句要实用、地道，覆盖不同用法
3. 提供至少 3 个例句
4. 词源和记忆技巧要有趣、易懂
5. 返回合法的 JSON 格式
"""

        return prompt

    def _parse_response(self, word: str, data: dict) -> LLMExplanation:
        """解析 LLM 返回的 JSON 数据"""
        # 解析例句
        examples = []
        for ex in data.get("examples", []):
            if isinstance(ex, dict):
                examples.append(
                    LLMExample(
                        sentence=ex.get("sentence", ""),
                        translation=ex.get("translation", "")
                    )
                )

        # 如果没有例句，创建一个默认例句
        if not examples:
            examples = [
                LLMExample(
                    sentence=f"Example with {word}.",
                    translation=f"使用 {word} 的例句。"
                )
            ]

        return LLMExplanation(
            word=word,
            pronunciation=data.get("pronunciation"),
            basic_translation=data.get("basic_translation", ""),
            detailed_explanation=data.get("detailed_explanation", ""),
            etymology=data.get("etymology"),
            memory_tips=data.get("memory_tips"),
            usage_notes=data.get("usage_notes"),
            common_collocations=data.get("common_collocations"),
            examples=examples,
            synonyms=data.get("synonyms"),
            antonyms=data.get("antonyms"),
            related_words=data.get("related_words"),
            difficulty_level=data.get("difficulty_level"),
            frequency=data.get("frequency")
        )
