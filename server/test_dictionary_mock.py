#!/usr/bin/env python3
"""
DictionaryService 真实 API 测试

用法:
    uv run python test_dictionary_mock.py
"""

import asyncio
from services.dictionary import DictionaryService
from models.word import WordDefinition


async def test_get_definition_success():
    """测试成功获取单词释义 - 使用真实 API"""
    print("\n" + "="*60)
    print("测试 1: 成功获取单词释义 (真实 API)")
    print("="*60)

    service = DictionaryService()

    try:
        # 调用真实 API
        result = await service.get_definition("result")

        # 验证结果
        print(f"result {result}")
        assert result.word == "result"

        print("✅ 所有断言通过!")
        print(f"   - 单词: {result.word}")
        print(f"   - 音标: {result.phonetic}")
        print(f"   - 词性数量: {len(result.meanings)}")
        print(f"   - 第一个释义: {result.meanings[0].definitions[0].definition[:50]}...")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def main():
    """运行所有测试"""
    print("="*60)
    print("DictionaryService 真实 API 测试")
    print("="*60)
    print("⚠️  注意: 测试使用真实的 Free Dictionary API")
    print("⚠️  如果 API 不可用，测试可能失败")
    print("="*60)

    tests = [
        ("成功获取单词释义", test_get_definition_success),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n✅ 通过: {passed}/{total}")
    if passed < total:
        print(f"❌ 失败: {total - passed}/{total}")

    print("\n详细结果:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {test_name}")

    print("\n" + "="*60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    import sys
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ 测试脚本错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
