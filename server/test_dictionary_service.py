#!/usr/bin/env python3
"""
测试 DictionaryService.get_definition 方法

用法:
    python3 test_dictionary_service.py
    或
    uv run python test_dictionary_service.py
"""

import asyncio
import sys
from services.dictionary import DictionaryService


async def test_word(service: DictionaryService, word: str):
    """测试单个单词查询"""
    print(f"\n{'='*60}")
    print(f"测试单词: {word}")
    print(f"{'='*60}")

    try:
        definition = await service.get_definition(word)

        print(f"✅ 查询成功!")
        print(f"\n单词: {definition.word}")
        print(f"音标: {definition.phonetic or '(无音标)'}")
        print(f"\n释义数量: {len(definition.meanings)}")

        for i, meaning in enumerate(definition.meanings, 1):
            print(f"\n【{i}】词性: {meaning.part_of_speech}")
            print(f"    定义数量: {len(meaning.definitions)}")

            for j, def_item in enumerate(meaning.definitions[:3], 1):  # 只显示前3个
                print(f"    {j}. {def_item.definition}")
                if def_item.example:
                    print(f"       例句: {def_item.example}")

        return True

    except ValueError as e:
        print(f"❌ 查询失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 意外错误: {type(e).__name__}: {e}")
        return False


async def main():
    """主测试函数"""
    print("="*60)
    print("DictionaryService.get_definition() 测试脚本")
    print("="*60)

    # 初始化服务
    service = DictionaryService()

    # 测试用例
    test_cases = [
        # 基本测试
        ("hello", "常用单词 - 应该成功"),
        ("test", "常用单词 - 应该成功"),
        ("python", "技术词汇 - 应该成功"),

        # 大小写测试
        ("Hello", "大写单词 - 测试 .lower() 处理"),
        ("WORLD", "全大写 - 测试 .lower() 处理"),

        # 边界情况
        ("a", "单字母 - 应该成功"),
        ("i", "单字母 - 应该成功"),

        # 错误情况
        ("asdfghjkl", "不存在的单词 - 应该失败"),
        ("123456", "纯数字 - 应该失败"),
        ("", "空字符串 - 应该失败"),
    ]

    results = []

    for word, description in test_cases:
        print(f"\n{description}")
        success = await test_word(service, word)
        results.append((word, description, success))

        # 稍微延迟，避免过快请求 API
        await asyncio.sleep(0.5)

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed = sum(1 for _, _, success in results if success)
    total = len(results)

    print(f"\n通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")

    print("\n详细结果:")
    for word, description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        word_display = f'"{word}"' if word else '(空)'
        print(f"  {status} - {word_display:15s} {description}")

    print("\n" + "="*60)

    # 返回退出码
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试脚本错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
