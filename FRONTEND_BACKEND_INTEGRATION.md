# 前后端集成说明

## 概述

Flutter 前端已成功对接 Python FastAPI 后端的 `/api/search` 接口，实现双向翻译功能。

---

## 🔗 API 对接

### 后端接口

**端点**: `POST http://localhost:3000/api/search`

**请求格式**:
```json
{
  "query": "hello"  // 或 "你好"
}
```

**响应格式**:
```json
{
  "query": "hello",
  "detected_language": "en",
  "result": {
    "word": "hello",
    "phonetic": "/həˈləʊ/",
    "chinese": "你好",
    "meanings": [
      {
        "part_of_speech": "noun",
        "definitions": [
          {
            "definition": "An utterance of 'hello'; a greeting.",
            "definition_chinese": "打招呼；问候",
            "example": "she was getting polite nods and hellos",
            "example_chinese": "她得到礼貌的点头和问候"
          }
        ]
      }
    ]
  },
  "english": null  // 如果输入是中文，这里会显示翻译后的英文
}
```

---

## 📱 前端实现

### 1. 数据模型

#### `SearchResponse` (新增)
```dart
// lib/models/search_response.dart
class SearchResponse {
  final String query;
  final String detectedLanguage;
  final WordDefinition result;
  final String? english;
}
```

#### `WordDefinition` (更新)
```dart
// lib/models/word_definition.dart
class WordDefinition {
  final String word;
  final String? phonetic;
  final String? chinese;          // ✨ 新增：中文翻译
  final List<Meaning> meanings;
  final String? translatedFrom;
}
```

#### `Definition` (更新)
```dart
class Definition {
  final String definition;
  final String? definitionChinese;  // ✨ 新增：释义中文翻译
  final String? example;
  final String? exampleChinese;     // ✨ 新增：例句中文翻译
}
```

### 2. API 服务

#### `DictionaryService.searchWord()`
```dart
// lib/services/dictionary_service.dart
Future<WordDefinition> searchWord(String query) async {
  final url = Uri.parse('${ApiConfig.baseUrl}/search');

  final response = await _client.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'query': query}),
  ).timeout(ApiConfig.timeout);

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    final searchResponse = SearchResponse.fromJson(data);
    return searchResponse.result;  // 返回 result 字段
  }

  throw DictionaryException('Failed to search');
}
```

### 3. UI 展示

#### 详情页更新
```dart
// lib/screens/word_detail_screen.dart

// 显示单词和中文翻译
Text(def.word)                      // "hello"
Text(def.chinese!)                  // "你好" ✨
Text(def.phonetic!)                 // "/həˈləʊ/"

// 显示释义和中文翻译
Text(definition.definition)         // "An utterance of 'hello'"
Text(definition.definitionChinese!) // "打招呼；问候" ✨

// 显示例句和中文翻译
Text(definition.example!)           // "she was getting..."
Text(definition.exampleChinese!)    // "她得到礼貌的..." ✨
```

---

## 🚀 使用方法

### 1. 启动后端

```bash
cd server
./run.sh
```

服务运行在 `http://localhost:3000`

### 2. 启动前端

```bash
cd app
flutter pub get
flutter run -d chrome  # Web
# 或
flutter run -d macos   # macOS
```

### 3. 测试搜索

#### 英文查询
1. 在搜索框输入 `hello`
2. 点击搜索或按回车
3. 查看结果：
   - 单词: **hello**
   - 中文: **你好**
   - 音标: **/həˈləʊ/**
   - 释义（英文+中文）
   - 例句（英文+中文）

#### 中文查询
1. 在搜索框输入 `你好`
2. 点击搜索或按回车
3. 后端自动翻译为 `hello` 并返回释义

---

## 🔧 配置说明

### API 配置
```dart
// lib/services/api_config.dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:3000/api';
  static const Duration timeout = Duration(seconds: 10);
}
```

**注意**:
- Web 开发时使用 `localhost`
- iOS/Android 真机调试时需改为电脑的 IP 地址
- 例如: `http://192.168.1.100:3000/api`

---

## 📊 数据流程

```
用户输入 "hello" 或 "你好"
         ↓
Flutter UI (HomeScreen)
         ↓
DictionaryService.searchWord()
         ↓
HTTP POST to /api/search
         ↓
Python Backend
  - 检测语言（中文/英文）
  - 如果是中文，翻译为英文
  - 调用 Free Dictionary API
  - 翻译所有释义和例句为中文
         ↓
返回 SearchResponse JSON
         ↓
解析为 SearchResponse 对象
         ↓
提取 result (WordDefinition)
         ↓
显示在 WordDetailScreen
  - 单词 + 中文翻译
  - 音标
  - 释义（英文+中文）
  - 例句（英文+中文）
```

---

## 🐛 常见问题

### Q: 连接失败 "Failed to connect to localhost:3000"

**A**: 检查后端是否运行
```bash
cd server
./run.sh
```

访问 http://localhost:3000/health 应返回 `{"status":"healthy"}`

### Q: iOS/Android 真机测试连接失败

**A**: 修改 API 配置为电脑 IP
```dart
// api_config.dart
static const String baseUrl = 'http://192.168.1.100:3000/api';
```

### Q: CORS 错误（Web 开发）

**A**: 后端已配置 CORS，允许所有来源：
```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q: 翻译服务不可用

**A**: 后端使用 `deep-translator` (Google Translate)，需要网络连接。如果 Free Dictionary API 或翻译服务不可用，会返回 404 错误。

---

## ✅ 测试检查清单

- [x] 后端服务启动成功
- [x] 前端能成功发送请求
- [x] 英文查询返回正确结果
- [x] 中文查询自动翻译并返回结果
- [x] UI 正确显示中文翻译
- [x] 释义的中文翻译显示正确
- [x] 例句的中文翻译显示正确
- [x] 错误处理正常（404、网络错误等）

---

## 📝 API 字段映射

| 后端字段 | 前端字段 | 说明 |
|---------|---------|------|
| `query` | `SearchResponse.query` | 原始查询 |
| `detected_language` | `SearchResponse.detectedLanguage` | 检测到的语言 |
| `result` | `SearchResponse.result` | 词典结果 |
| `result.word` | `WordDefinition.word` | 英文单词 |
| `result.phonetic` | `WordDefinition.phonetic` | 音标 |
| `result.chinese` | `WordDefinition.chinese` | ✨ 中文翻译 |
| `part_of_speech` | `Meaning.partOfSpeech` | 词性 |
| `definition` | `Definition.definition` | 英文释义 |
| `definition_chinese` | `Definition.definitionChinese` | ✨ 释义中文 |
| `example` | `Definition.example` | 英文例句 |
| `example_chinese` | `Definition.exampleChinese` | ✨ 例句中文 |

---

## 🎯 下一步优化

1. **添加收藏功能**
   - 对接 `/api/favorites` 接口
   - 实现本地收藏列表

2. **优化用户体验**
   - 添加加载动画
   - 支持离线缓存
   - 添加搜索历史

3. **性能优化**
   - 实现结果缓存
   - 防抖搜索输入

---

## 📚 相关文档

- **后端 API 文档**: http://localhost:3000/docs
- **后端 README**: `server/README.md`
- **UV 使用指南**: `server/UV_GUIDE.md`
- **依赖修复说明**: `server/DEPENDENCY_FIX.md`

---

**集成完成！** ✨ 前后端已成功连接，双向翻译功能正常工作。
