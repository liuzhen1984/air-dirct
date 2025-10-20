import sqlite3
import os
from typing import Optional, List
from models.word import WordDefinition, Meaning, Definition


class DictionaryService:
    """词典服务 - 使用本地 ECDICT 数据库"""

    def __init__(self):
        # 数据库路径
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "dict",
            "stardict.db"
        )
        self.db_path = db_path

        # 检查数据库是否存在
        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"ECDICT database not found at {db_path}. "
                "Please download it first."
            )

    def _get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    async def get_definition(self, word: str) -> WordDefinition:
        """
        从本地数据库获取单词释义

        Args:
            word: 英文单词

        Returns:
            WordDefinition: 单词释义

        Raises:
            ValueError: 单词未找到
        """
        try:
            print(f"start find word {word} in local database")

            # 转换为小写查询
            word_lower = word.lower().strip()

            conn = self._get_connection()
            cursor = conn.cursor()

            # 查询单词
            cursor.execute(
                """
                SELECT word, phonetic, pos, translation, definition, detail
                FROM stardict
                WHERE word = ? COLLATE NOCASE
                LIMIT 1
                """,
                (word_lower,)
            )

            row = cursor.fetchone()
            conn.close()

            if not row:
                print(f"Failed to get word {word} from local database")
                raise ValueError(f"Word not found: {word}")

            print(f"get word {word} from local database: SUCCESS")

            # 解析数据
            db_word, phonetic, pos, translation, definition, detail = row

            # 构建返回结构
            return self._transform_response(
                db_word, phonetic, pos, translation, definition, detail
            )

        except ValueError:
            raise
        except Exception as e:
            print(f"Error querying database: {e}")
            raise ValueError(f"Failed to fetch definition: {str(e)}")

    def _transform_response(
        self,
        word: str,
        phonetic: Optional[str],
        pos: Optional[str],
        translation: Optional[str],
        definition: Optional[str],
        detail: Optional[str]
    ) -> WordDefinition:
        """
        转换 ECDICT 数据为内部数据格式

        ECDICT 字段说明:
        - word: 单词
        - phonetic: 音标 (例如: "hә'lәu")
        - pos: 词性标签 (例如: "u:97/n:3" 表示感叹词97%，名词3%)
        - translation: 中文翻译 (例如: "interj. 喂, 嘿")
        - definition: 英文释义 (例如: "n. an expression of greeting")
        - detail: 详细释义 (JSON 格式，可选)
        """

        # 格式化音标
        formatted_phonetic = None
        if phonetic:
            # 如果没有斜杠，添加斜杠
            if not phonetic.startswith('/'):
                formatted_phonetic = f"/{phonetic}/"
            else:
                formatted_phonetic = phonetic

        meanings = []

        # 解析 translation (中文) 和 definition (英文)
        # 格式: "n. 释义1; 释义2 \n v. 释义3"
        if translation or definition:
            # 合并中英文释义
            combined_text = ""
            if translation:
                combined_text = translation
            if definition:
                if combined_text:
                    combined_text += "\n" + definition
                else:
                    combined_text = definition

            # 按词性分组
            meanings = self._parse_definitions(combined_text)

        # 如果没有解析出任何释义，使用原始文本
        if not meanings:
            meanings = [
                Meaning(
                    part_of_speech="general",
                    definitions=[
                        Definition(
                            definition=definition or "No definition available",
                            definition_chinese=translation,
                            example=None,
                            example_chinese=None
                        )
                    ]
                )
            ]

        return WordDefinition(
            word=word,
            phonetic=formatted_phonetic,
            chinese=self._extract_chinese_only(translation),
            meanings=meanings
        )

    def _extract_chinese_only(self, translation: Optional[str]) -> Optional[str]:
        """
        提取纯中文翻译（去掉词性标记）

        例如: "interj. 喂, 嘿" -> "喂, 嘿"
        """
        if not translation:
            return None

        import re
        # 移除词性标记 (n. v. adj. 等)
        chinese = re.sub(r'^[a-z]+\.\s*', '', translation, flags=re.IGNORECASE)
        # 如果有多个词性，取第一个
        chinese = chinese.split('\n')[0].strip()
        return chinese if chinese else None

    def _parse_definitions(self, text: str) -> List[Meaning]:
        """
        解析释义文本，按词性分组

        输入格式示例:
        "n. 测试; 考验\nv. 测试; 检验"
        或
        "interj. 喂, 嘿"
        """
        meanings = []
        current_pos = None
        current_defs = []

        import re

        # 分割成行
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 匹配词性标记 (n. v. adj. adv. prep. conj. interj. 等)
            pos_match = re.match(r'^([a-z]+)\.\s+(.+)', line, re.IGNORECASE)

            if pos_match:
                # 保存之前的词性
                if current_pos and current_defs:
                    meanings.append(
                        Meaning(
                            part_of_speech=current_pos,
                            definitions=current_defs
                        )
                    )

                # 开始新的词性
                current_pos = self._normalize_pos(pos_match.group(1))
                definition_text = pos_match.group(2)

                # 分割多个释义 (用分号或逗号)
                parts = re.split(r'[;；,，]', definition_text)
                current_defs = [
                    Definition(
                        definition=part.strip(),
                        definition_chinese=part.strip(),  # ECDICT 已经是中文
                        example=None,
                        example_chinese=None
                    )
                    for part in parts if part.strip()
                ]
            else:
                # 没有词性标记，作为通用释义
                if not current_pos:
                    current_pos = "general"
                    current_defs = []

                current_defs.append(
                    Definition(
                        definition=line,
                        definition_chinese=line,
                        example=None,
                        example_chinese=None
                    )
                )

        # 保存最后一个词性
        if current_pos and current_defs:
            meanings.append(
                Meaning(
                    part_of_speech=current_pos,
                    definitions=current_defs
                )
            )

        return meanings

    def _normalize_pos(self, pos: str) -> str:
        """
        标准化词性标记

        n -> noun
        v -> verb
        adj -> adjective
        等
        """
        pos_map = {
            'n': 'noun',
            'v': 'verb',
            'adj': 'adjective',
            'adv': 'adverb',
            'prep': 'preposition',
            'conj': 'conjunction',
            'interj': 'interjection',
            'pron': 'pronoun',
            'art': 'article',
            'det': 'determiner',
            'num': 'numeral',
        }

        return pos_map.get(pos.lower(), pos)

    def search_words(self, prefix: str, limit: int = 10) -> List[str]:
        """
        搜索以指定前缀开头的单词（用于自动补全）

        Args:
            prefix: 单词前缀
            limit: 返回数量限制

        Returns:
            List[str]: 单词列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT word
            FROM stardict
            WHERE word LIKE ? COLLATE NOCASE
            ORDER BY word
            LIMIT ?
            """,
            (f"{prefix}%", limit)
        )

        words = [row[0] for row in cursor.fetchall()]
        conn.close()

        return words
