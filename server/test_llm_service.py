#!/usr/bin/env python3
"""
LLM Service 测试脚本

测试 OpenAI API 集成和 LLM 增强词典功能

用法:
    # 确保已设置 OPENAI_API_KEY 环境变量
    export OPENAI_API_KEY=sk-xxx...

    # 运行测试
    uv run python test_llm_service.py
"""

import asyncio
import os
from services.llm_service import LLMService
from models.llm_response import LLMExplanation


async def test_llm_explain_simple():
    """测试简单单词解释"""
    print("\n" + "="*60)
    print("测试 1: 简单单词解释 - 'hello'")
    print("="*60)

    try:
        service = LLMService()
        result = await service.explain_word("hello")

        # 验证返回结构
        assert isinstance(result, LLMExplanation)
        assert result.word == "hello"
        assert result.basic_translation
        assert result.detailed_explanation
        assert len(result.examples) >= 1

        print("✅ 测试通过!")
        print(f"\n单词: {result.word}")
        print(f"音标: {result.pronunciation}")
        print(f"基础翻译: {result.basic_translation}")
        print(f"详细解释: {result.detailed_explanation}")
        print(f"\n例句数量: {len(result.examples)}")
        for i, ex in enumerate(result.examples[:2], 1):
            print(f"  例句 {i}: {ex.sentence}")
            print(f"  翻译: {ex.translation}")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_llm_explain_with_basic():
    """测试带基础释义的单词解释"""
    print("\n" + "="*60)
    print("测试 2: 带基础释义的单词解释 - 'algorithm'")
    print("="*60)

    try:
        service = LLMService()
        basic_def = "算法; 运算法则"
        result = await service.explain_word("algorithm", basic_def)

        assert isinstance(result, LLMExplanation)
        assert result.word == "algorithm"
        assert result.detailed_explanation
        assert len(result.examples) >= 1

        print("✅ 测试通过!")
        print(f"\n单词: {result.word}")
        print(f"基础翻译: {result.basic_translation}")
        print(f"详细解释: {result.detailed_explanation}")

        if result.etymology:
            print(f"\n词源: {result.etymology}")
        if result.memory_tips:
            print(f"记忆技巧: {result.memory_tips}")
        if result.synonyms:
            print(f"近义词: {', '.join(result.synonyms)}")

        print(f"\n例句:")
        for i, ex in enumerate(result.examples, 1):
            print(f"  {i}. {ex.sentence}")
            print(f"     {ex.translation}")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_llm_complex_word():
    """测试复杂单词"""
    print("\n" + "="*60)
    print("测试 3: 复杂单词 - 'serendipity'")
    print("="*60)

    try:
        service = LLMService()
        result = await service.explain_word("serendipity")

        assert isinstance(result, LLMExplanation)
        assert result.word == "serendipity"

        print("✅ 测试通过!")
        print(f"\n单词: {result.word}")
        print(f"音标: {result.pronunciation}")
        print(f"基础翻译: {result.basic_translation}")
        print(f"详细解释: {result.detailed_explanation}")

        if result.etymology:
            print(f"\n词源: {result.etymology}")
        if result.memory_tips:
            print(f"记忆技巧: {result.memory_tips}")
        if result.difficulty_level:
            print(f"难度: {result.difficulty_level}")
        if result.frequency:
            print(f"词频: {result.frequency}")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_key_missing():
    """测试缺少 API Key 的情况"""
    print("\n" + "="*60)
    print("测试 4: 检查 API Key 配置")
    print("="*60)

    original_key = os.getenv("OPENAI_API_KEY")

    try:
        # 临时移除 API Key
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # 应该抛出错误
        service = LLMService()
        print("❌ 应该抛出 ValueError")
        return False

    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            print(f"✅ 正确检测到缺少 API Key: {e}")
            return True
        else:
            print(f"❌ 错误信息不正确: {e}")
            return False

    finally:
        # 恢复 API Key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key


async def main():
    """运行所有测试"""
    print("="*60)
    print("LLM Service 测试")
    print("="*60)

    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("\n⚠️  警告: 未设置有效的 OPENAI_API_KEY")
        print("请先设置环境变量:")
        print("  export OPENAI_API_KEY=sk-xxx...")
        print("\n跳过需要 API 的测试，只运行配置检查...\n")

        # 只运行 API Key 检查测试
        tests = [
            ("API Key 检查", test_api_key_missing),
        ]
    else:
        print(f"\n✅ API Key 已配置")
        print(f"   Model: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")

        if base_url := os.getenv("OPENAI_BASE_URL"):
            print(f"   Base URL: {base_url}")

        # 运行所有测试
        tests = [
            ("简单单词解释", test_llm_explain_simple),
            ("带基础释义的解释", test_llm_explain_with_basic),
            ("复杂单词解释", test_llm_complex_word),
            ("API Key 检查", test_api_key_missing),
        ]

    results = []

    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
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
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试脚本错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
