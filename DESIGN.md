# 轻量级英文词典应用 - 设计文档

## 项目概述

一个简洁、快速的英文词典 Web 应用，采用类似 Google 首页的极简设计风格，支持多语言输入并提供英文释义。

### 核心特性
- 极简 UI：单一搜索框 + 智能历史记录
- 多语言支持：接受任意语言输入，自动翻译为英文并提供释义
- 智能去重：历史记录自动合并相似单词
- 快速查询：本地缓存 + API 调用优化

---

## 1. 功能需求

### 1.1 首页设计
```
┌─────────────────────────────────────┐
│                                     │
│          [Logo/Title]               │
│                                     │
│    ┌───────────────────────────┐   │
│    │  Search here...           │   │
│    └───────────────────────────┘   │
│                                     │
│    Recent Searches:                 │
│    • history                        │
│    • translate                      │
│    • 翻译                           │
│                                     │
└─────────────────────────────────────┘
```

**关键元素：**
- 搜索框：居中显示，支持即时搜索（可选防抖）
- 历史记录：显示 1-5 个最近查询，点击可快速查询
- 响应式设计：移动端友好

### 1.2 搜索功能

**输入类型处理：**
1. **英文输入** → 显示英文释义、词性、例句
2. **非英文输入**（中文、日文等）→ 先翻译为英文，再显示释义

**搜索流程：**
```
用户输入 → 语言检测 → 英文释义查询 → 结果展示
            ↓
        (非英文) → 翻译为英文 → 英文释义查询
```

### 1.3 智能历史记录去重

**去重策略：**
1. **编辑距离算法**（Levenshtein Distance）
   - `history` vs `histroy` → 相似度高，保留一个
   - 阈值设定：距离 ≤ 2 视为相似

2. **词形还原**（Lemmatization）
   - `running`, `runs`, `ran` → 都还原为 `run`
   - 使用 NLP 库（如 `compromise` 或 `natural`）

3. **优先级规则：**
   - 保留最近查询的版本
   - 保留正确拼写版本（通过字典验证）

**存储结构：**
```javascript
{
  "history": [
    {
      "word": "history",
      "lemma": "history",
      "timestamp": 1697456789000,
      "variants": ["histroy", "historie"]  // 合并的相似词
    }
  ]
}
```

---

## 2. 技术架构

### 2.1 技术栈

**前端：**
- **框架**：React 18+ / Vue 3（建议 React + Vite）
- **样式**：Tailwind CSS（快速实现极简设计）
- **状态管理**：Zustand / Jotai（轻量级）
- **HTTP 客户端**：Axios

**后端（可选）：**
- **方案 1**：纯前端（直接调用第三方 API）
- **方案 2**：Node.js + Express（中间层，API 聚合 + 缓存）

### 2.2 API 选择

**词典 API：**
1. **Free Dictionary API**（免费，无需 Key）
   - URL: `https://api.dictionaryapi.dev/api/v2/entries/en/{word}`
   - 优点：免费、稳定
   - 缺点：仅支持英文查询

2. **Merriam-Webster API**（需注册，免费额度）
   - 提供详细释义、音标、例句

**翻译 API：**
1. **LibreTranslate**（开源，自托管或公共实例）
   - URL: `https://libretranslate.com/translate`
   - 支持多语言 ↔ 英文

2. **Google Translate API**（付费，但有免费额度）
   - 备选方案：MyMemory Translation API（免费）

### 2.3 系统架构图

```
┌──────────────┐
│   用户界面   │
│   (React)    │
└──────┬───────┘
       │
       ├──→ 本地存储 (IndexedDB/LocalStorage)
       │    └─ 历史记录、缓存
       │
       ├──→ 语言检测模块
       │    └─ franc.js (轻量级语言识别)
       │
       ├──→ 词形还原模块
       │    └─ compromise.js
       │
       └──→ API 层
            ├─ 词典 API (Free Dictionary)
            └─ 翻译 API (LibreTranslate)
```

---

## 3. 核心模块设计

### 3.1 搜索模块

```typescript
interface SearchService {
  // 主搜索方法
  search(query: string): Promise<SearchResult>;

  // 语言检测
  detectLanguage(text: string): string;

  // 翻译（如果需要）
  translate(text: string, targetLang: string): Promise<string>;

  // 获取词典释义
  getDefinition(word: string): Promise<Definition>;
}

interface SearchResult {
  originalQuery: string;      // 原始输入
  translatedQuery?: string;   // 翻译后的英文（如适用）
  language: string;           // 检测到的语言
  definition: Definition;     // 词典释义
}

interface Definition {
  word: string;
  phonetic?: string;
  meanings: Array<{
    partOfSpeech: string;     // 词性（名词、动词等）
    definitions: Array<{
      definition: string;
      example?: string;
    }>;
  }>;
}
```

### 3.2 历史记录模块

```typescript
interface HistoryService {
  // 添加记录（自动去重）
  addToHistory(word: string): void;

  // 获取历史记录（1-5 条）
  getHistory(limit: number): HistoryItem[];

  // 清空历史
  clearHistory(): void;
}

interface HistoryItem {
  word: string;              // 标准单词
  lemma: string;             // 词根
  timestamp: number;         // 时间戳
  variants: string[];        // 相似词变体
  frequency: number;         // 查询频率
}

// 去重算法
class DeduplicationEngine {
  // 计算编辑距离
  levenshteinDistance(a: string, b: string): number;

  // 词形还原
  lemmatize(word: string): string;

  // 合并相似词
  mergeIfSimilar(
    newWord: string,
    existingHistory: HistoryItem[]
  ): HistoryItem[];
}
```

**去重逻辑流程：**
```javascript
function addToHistory(newWord) {
  const lemma = lemmatize(newWord);

  // 1. 查找是否存在相似词
  const similar = history.find(item => {
    return item.lemma === lemma ||
           levenshteinDistance(item.word, newWord) <= 2;
  });

  // 2. 如果存在，更新记录
  if (similar) {
    similar.variants.push(newWord);
    similar.timestamp = Date.now();
    similar.frequency++;
  } else {
    // 3. 新增记录
    history.unshift({
      word: newWord,
      lemma,
      timestamp: Date.now(),
      variants: [],
      frequency: 1
    });
  }

  // 4. 保持最多 50 条（展示前 5 条）
  history = history.slice(0, 50);
  saveToLocalStorage(history);
}
```

### 3.3 缓存模块

```typescript
interface CacheService {
  // 获取缓存
  get(key: string): Promise<any | null>;

  // 设置缓存（带过期时间）
  set(key: string, value: any, ttl?: number): Promise<void>;

  // 清空缓存
  clear(): Promise<void>;
}

// 使用 IndexedDB 实现持久化缓存
// TTL: 7 天（词典释义变化不频繁）
```

---

## 4. 用户界面设计

### 4.1 首页布局

```jsx
<div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
  {/* Logo */}
  <h1 className="text-4xl font-light mb-8">Dict</h1>

  {/* 搜索框 */}
  <div className="w-full max-w-2xl px-4">
    <input
      type="text"
      placeholder="Enter a word in any language..."
      className="w-full px-6 py-4 text-lg border-2 rounded-full
                 focus:outline-none focus:border-blue-500"
      onKeyDown={handleSearch}
    />
  </div>

  {/* 历史记录 */}
  {history.length > 0 && (
    <div className="mt-8 flex gap-3">
      {history.slice(0, 5).map(item => (
        <button
          key={item.word}
          className="px-4 py-2 bg-white rounded-full shadow-sm
                     hover:shadow-md transition"
          onClick={() => searchWord(item.word)}
        >
          {item.word}
          {item.variants.length > 0 && (
            <span className="ml-2 text-gray-400 text-sm">
              +{item.variants.length}
            </span>
          )}
        </button>
      ))}
    </div>
  )}
</div>
```

### 4.2 结果页面

```jsx
<div className="max-w-4xl mx-auto p-6">
  {/* 头部信息 */}
  <div className="mb-6">
    <h2 className="text-3xl font-bold">{result.word}</h2>
    {result.phonetic && (
      <p className="text-gray-600 mt-2">{result.phonetic}</p>
    )}
    {result.translatedQuery && (
      <p className="text-sm text-blue-600 mt-1">
        Translated from: {result.originalQuery}
      </p>
    )}
  </div>

  {/* 释义列表 */}
  {result.meanings.map((meaning, idx) => (
    <div key={idx} className="mb-6">
      <h3 className="text-xl font-semibold text-gray-700 mb-3">
        {meaning.partOfSpeech}
      </h3>
      <ol className="list-decimal list-inside space-y-2">
        {meaning.definitions.map((def, i) => (
          <li key={i} className="text-gray-800">
            {def.definition}
            {def.example && (
              <p className="text-gray-500 italic ml-6 mt-1">
                "{def.example}"
              </p>
            )}
          </li>
        ))}
      </ol>
    </div>
  ))}
</div>
```

### 4.3 移动端适配

- 搜索框：宽度 100%，字体 16px（避免 iOS 自动缩放）
- 历史记录：横向滚动或纵向堆叠
- 响应式断点：
  - Mobile: < 640px
  - Tablet: 640-1024px
  - Desktop: > 1024px

---

## 5. 数据流设计

### 5.1 搜索流程

```
1. 用户输入 "history" 并按回车
   ↓
2. 检查本地缓存
   - 命中 → 直接返回结果
   - 未命中 → 继续
   ↓
3. 语言检测（franc.js）
   - 检测为英文 → 跳到步骤 5
   - 检测为其他语言 → 继续
   ↓
4. 调用翻译 API
   - 翻译为英文
   ↓
5. 调用词典 API
   - 获取释义
   ↓
6. 缓存结果
   ↓
7. 添加到历史记录（智能去重）
   ↓
8. 展示结果
```

### 5.2 历史记录更新流程

```
新查询: "histroy"
   ↓
1. 词形还原 → "history"
   ↓
2. 检查现有历史:
   - 已存在 "history" (lemma: "history")
   ↓
3. 合并操作:
   - 将 "histroy" 添加到 variants
   - 更新 timestamp
   - frequency++
   ↓
4. 不新增记录，保持列表简洁
```

---

## 6. 性能优化

### 6.1 前端优化
- **防抖**：搜索框输入 300ms 后再触发（可选实时建议）
- **懒加载**：历史记录仅加载前 5 条
- **虚拟滚动**：结果页面长释义列表
- **代码分割**：按路由拆分 bundle

### 6.2 API 优化
- **缓存策略**：
  - 词典结果：7 天 TTL
  - 翻译结果：1 天 TTL（翻译可能更新）
- **请求合并**：使用 `Promise.all()` 并行调用
- **错误处理**：API 失败时显示友好提示

### 6.3 存储优化
- **IndexedDB**：存储大量缓存数据
- **LocalStorage**：存储历史记录（轻量级，上限 5MB）
- **定期清理**：过期缓存自动删除

---

## 7. 实现路线图

### Phase 1: MVP（最小可行产品）
- [ ] 基础 UI：搜索框 + 历史记录展示
- [ ] 英文词典查询（Free Dictionary API）
- [ ] 简单历史记录（无去重）
- [ ] 本地存储（LocalStorage）

### Phase 2: 核心功能
- [ ] 集成翻译 API（支持多语言输入）
- [ ] 智能去重算法实现
  - [ ] 编辑距离计算
  - [ ] 词形还原
- [ ] 缓存系统（IndexedDB）
- [ ] 响应式设计优化

### Phase 3: 增强体验
- [ ] 搜索建议（自动完成）
- [ ] 发音播放（TTS API）
- [ ] 深色模式
- [ ] 快捷键支持（如 `/` 聚焦搜索）
- [ ] PWA 支持（离线使用）

### Phase 4: 高级功能
- [ ] 用户账户（同步历史记录）
- [ ] 生词本功能
- [ ] 导出历史记录
- [ ] 多词典源对比

---

## 8. 技术挑战与解决方案

### 挑战 1：智能去重的准确性
**问题**：如何平衡去重激进度？
- 太激进：`cat` 和 `car` 被合并（误判）
- 太保守：`history` 和 `histroy` 分开（冗余）

**解决方案**：
```javascript
function shouldMerge(word1, word2) {
  const distance = levenshteinDistance(word1, word2);
  const maxLength = Math.max(word1.length, word2.length);

  // 1. 短单词更严格（距离 ≤ 1）
  if (maxLength <= 4) return distance <= 1;

  // 2. 长单词宽松（距离 ≤ 2）
  if (maxLength > 4) return distance <= 2;

  // 3. 词根相同直接合并
  return lemmatize(word1) === lemmatize(word2);
}
```

### 挑战 2：跨语言翻译的准确性
**问题**：翻译 API 可能返回不准确结果

**解决方案**：
- 显示原始输入和翻译结果，让用户验证
- 支持手动编辑翻译结果
- 使用多个翻译源（主备机制）

### 挑战 3：API 限流
**问题**：免费 API 有请求限制

**解决方案**：
- 激进缓存策略（减少重复请求）
- 实现请求队列（控制并发）
- 提供降级方案（离线模式）

---

## 9. 安全与隐私

### 9.1 数据安全
- **本地存储**：所有数据存储在用户浏览器
- **无后端**：不收集用户查询数据
- **HTTPS**：强制使用加密连接

### 9.2 API Key 保护
- 使用环境变量存储（`.env`）
- 部署时配置密钥管理服务
- 考虑后端代理隐藏 Key

---

## 10. 测试策略

### 10.1 单元测试
- 去重算法测试
- 语言检测测试
- 缓存逻辑测试

### 10.2 集成测试
- API 调用流程
- 历史记录同步

### 10.3 E2E 测试
- 完整搜索流程
- 多设备兼容性

---

## 11. 部署方案

### 推荐部署平台
1. **Vercel**（推荐，零配置）
   - 自动 CI/CD
   - 全球 CDN
   - 免费 HTTPS

2. **Netlify**（备选）
   - 类似 Vercel
   - 支持表单处理

3. **GitHub Pages**（纯静态）
   - 完全免费
   - 需要配置 CI

---

## 12. 后续扩展

### 可选功能
- **语音输入**：Web Speech API
- **OCR 识别**：上传图片识别单词
- **例句来源**：链接到权威词典
- **协作功能**：分享查询结果

### 商业化考虑
- **高级版**：无限历史、多设备同步、优质 API
- **广告**：免费版底部展示
- **API 服务**：提供给第三方开发者

---

## 附录

### A. 依赖库推荐

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-router-dom": "^6.x",
    "axios": "^1.x",
    "zustand": "^4.x",
    "franc": "^6.x",           // 语言检测
    "compromise": "^14.x",     // NLP（词形还原）
    "idb": "^7.x"              // IndexedDB 包装器
  },
  "devDependencies": {
    "vite": "^5.x",
    "tailwindcss": "^3.x",
    "vitest": "^1.x"
  }
}
```

### B. 编辑距离算法实现

```javascript
function levenshteinDistance(a, b) {
  const matrix = Array(b.length + 1)
    .fill(null)
    .map(() => Array(a.length + 1).fill(null));

  for (let i = 0; i <= a.length; i++) matrix[0][i] = i;
  for (let j = 0; j <= b.length; j++) matrix[j][0] = j;

  for (let j = 1; j <= b.length; j++) {
    for (let i = 1; i <= a.length; i++) {
      const indicator = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1,       // 删除
        matrix[j - 1][i] + 1,       // 插入
        matrix[j - 1][i - 1] + indicator  // 替换
      );
    }
  }

  return matrix[b.length][a.length];
}
```

### C. API 使用示例

**Free Dictionary API：**
```javascript
// GET https://api.dictionaryapi.dev/api/v2/entries/en/hello
{
  "word": "hello",
  "phonetic": "/həˈləʊ/",
  "meanings": [
    {
      "partOfSpeech": "noun",
      "definitions": [
        {
          "definition": "\"Hello!\" or an equivalent greeting.",
          "example": "she was getting polite nods and hellos from people"
        }
      ]
    }
  ]
}
```

**LibreTranslate API：**
```javascript
// POST https://libretranslate.com/translate
{
  "q": "你好",
  "source": "zh",
  "target": "en"
}
// Response: { "translatedText": "Hello" }
```

---

## 版本历史

- **v1.0** (2024-10-16): 初始设计文档
  - 定义核心功能和架构
  - 详细设计去重算法
  - 规划实现路线图

---

**文档作者**: Claude
**创建日期**: 2024-10-16
**状态**: Draft
**审核者**: 待定