#!/usr/bin/env python3
"""
DictionaryService 简单快速测试

用法:
    uv run python test_dictionary_simple.py
"""

import asyncio
from services.dictionary import DictionaryService


async def main():
    """简单测试 - 只测试一个单词"""
    print("="*60)
    print("测试 DictionaryService.get_definition()")
    print("="*60)

    service = DictionaryService()

    # 测试单词
    word = "test"

    print(f"\n📝 查询单词: {word}")
    print("⏳ 请稍等...")

    try:
        definition = await service.get_definition(word)

        print(f"\n✅ 查询成功!")
        print(f"\n单词: {definition.word}")
        print(f"音标: {definition.phonetic}")

        print(f"\n找到 {len(definition.meanings)} 个词性:")

        for i, meaning in enumerate(definition.meanings, 1):
            print(f"\n【{i}】{meaning.part_of_speech}")
            print(f"  共 {len(meaning.definitions)} 个释义")

            # 显示第一个释义
            if meaning.definitions:
                first_def = meaning.definitions[0]
                print(f"  1. {first_def.definition}")
                if first_def.example:
                    print(f"     💬 {first_def.example}")

        print(f"\n{'='*60}")
        print("✅ 测试通过!")
        return 0

    except ValueError as e:
        print(f"\n❌ 查询失败: {e}")
        return 1

    except Exception as e:
        print(f"\n❌ 意外错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被中断")
        sys.exit(1)
