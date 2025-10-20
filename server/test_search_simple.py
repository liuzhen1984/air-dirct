"""
测试简化版搜索接口
"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from models.search import SearchRequest
from api.search import search_word


async def test_english_word():
    """测试英文单词查询"""
    print("=" * 60)
    print("测试1: 查询英文单词 'hello'")
    print("=" * 60)

    request = SearchRequest(query="hello")
    response = await search_word(request)

    print(f"\n查询: {response.query}")
    print(f"是否中文: {response.is_chinese}")

    if response.english_result:
        result = response.english_result
        print(f"单词: {result.word}")
        print(f"音标: {result.phonetic}")
        print(f"释义:")
        for meaning in result.meanings:
            print(f"  [{meaning.pos}] {meaning.meaning}")

    print()


async def test_chinese_word():
    """测试中文翻译"""
    print("=" * 60)
    print("测试2: 翻译中文 '你好'")
    print("=" * 60)

    request = SearchRequest(query="你好")
    response = await search_word(request)

    print(f"\n查询: {response.query}")
    print(f"是否中文: {response.is_chinese}")

    if response.chinese_result:
        print(f"英文翻译: {', '.join(response.chinese_result.translations)}")

    print()


async def test_chinese_phrase():
    """测试中文短语"""
    print("=" * 60)
    print("测试3: 翻译中文短语 '苹果'")
    print("=" * 60)

    request = SearchRequest(query="苹果")
    response = await search_word(request)

    print(f"\n查询: {response.query}")
    print(f"是否中文: {response.is_chinese}")

    if response.chinese_result:
        print(f"英文翻译: {', '.join(response.chinese_result.translations)}")

    print()


async def test_english_word_test():
    """测试英文单词 test"""
    print("=" * 60)
    print("测试4: 查询英文单词 'test'")
    print("=" * 60)

    request = SearchRequest(query="test")
    response = await search_word(request)

    print(f"\n查询: {response.query}")
    print(f"是否中文: {response.is_chinese}")

    if response.english_result:
        result = response.english_result
        print(f"单词: {result.word}")
        print(f"音标: {result.phonetic}")
        print(f"释义:")
        for meaning in result.meanings:
            print(f"  [{meaning.pos}] {meaning.meaning}")

    print()


async def main():
    """运行所有测试"""
    try:
        await test_english_word()
        await test_chinese_word()
        await test_chinese_phrase()
        await test_english_word_test()

        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
