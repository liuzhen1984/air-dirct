# 搜索接口 API 示例

## 接口地址
POST `/api/search`

## 请求格式
```json
{
  "query": "单词或短语"
}
```

## 响应格式

### 1. 英文输入 - 从本地库查询

**请求:**
```json
{
  "query": "hello"
}
```

**响应:**
```json
{
  "query": "hello",
  "is_chinese": false,
  "english_result": {
    "word": "hello",
    "phonetic": "/hә'lәu/",
    "meanings": [
      {
        "pos": "interjection",
        "meaning": "喂; 嘿"
      },
      {
        "pos": "noun",
        "meaning": "an expression of greeting"
      }
    ]
  },
  "chinese_result": null
}
```

### 2. 英文输入 - 复杂词汇

**请求:**
```json
{
  "query": "test"
}
```

**响应:**
```json
{
  "query": "test",
  "is_chinese": false,
  "english_result": {
    "word": "test",
    "phonetic": "/test/",
    "meanings": [
      {
        "pos": "noun",
        "meaning": "测试; 试验; 化验; 检验; 考验; 甲壳"
      },
      {
        "pos": "verb",
        "meaning": "测试; 试验; 化验"
      }
    ]
  },
  "chinese_result": null
}
```

### 3. 中文输入 - 直接翻译

**请求:**
```json
{
  "query": "你好"
}
```

**响应:**
```json
{
  "query": "你好",
  "is_chinese": true,
  "english_result": null,
  "chinese_result": {
    "translations": ["Hello"]
  }
}
```

**请求:**
```json
{
  "query": "苹果"
}
```

**响应:**
```json
{
  "query": "苹果",
  "is_chinese": true,
  "english_result": null,
  "chinese_result": {
    "translations": ["apple"]
  }
}
```

### 4. 中文输入 - 多个翻译结果

如果Google翻译返回多个结果(用逗号分隔),会自动拆分:

**响应示例:**
```json
{
  "query": "银行",
  "is_chinese": true,
  "english_result": null,
  "chinese_result": {
    "translations": ["bank", "banking"]
  }
}
```

## 字段说明

### SearchResponse
- `query` (string): 用户输入的查询内容
- `is_chinese` (boolean): 是否为中文输入
- `english_result` (EnglishResult | null): 英文查询结果(仅英文输入时有值)
- `chinese_result` (ChineseResult | null): 中文翻译结果(仅中文输入时有值)

### EnglishResult
- `word` (string): 单词
- `phonetic` (string | null): 音标
- `meanings` (Array<SimpleMeaning>): 词义列表

### SimpleMeaning
- `pos` (string): 词性 (noun, verb, adjective等)
- `meaning` (string): 中文释义 (多个释义用分号分隔)

### ChineseResult
- `translations` (Array<string>): 英文翻译列表

## 错误处理

### 404 - 单词未找到
```json
{
  "detail": "Word not found: xyz"
}
```

## 特性

1. **英文输入**:
   - 使用本地ECDICT数据库
   - 无需网络请求,速度快
   - 提供音标和按词性分组的中文释义

2. **中文输入**:
   - 使用GoogleTranslate在线翻译
   - 支持多个翻译结果
   - 直接返回英文,无需额外查询

3. **简化格式**:
   - 移除了不必要的例句和详细信息
   - 词义按词性合并为一个字符串
   - 响应结构清晰,易于前端处理
