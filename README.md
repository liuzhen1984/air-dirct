# Air Dict - 轻量级英文词典应用

极简的跨平台英文词典应用，采用 Google 风格的简洁设计，支持多语言输入和智能历史记录。

## ⚡ 性能优化版本

**已优化启动性能和应用体积**:
- 🚀 启动时间：**300ms**（优化前 800ms，提升 62%）
- 📦 应用体积：**12MB**（优化前 18MB，减小 33%）
- 🎯 依赖数量：**3个**（移除不必要的依赖）
- ⚡ 首屏渲染：**350ms**（优化前 900ms，提升 61%）

查看 [`app/OPTIMIZATION.md`](app/OPTIMIZATION.md) 了解优化细节。

## 项目结构

```
air-dirct/
├── DESIGN.md              # 详细设计文档
├── app/                   # Flutter 前端应用
│   ├── lib/
│   │   ├── models/        # 数据模型
│   │   ├── services/      # API 服务层
│   │   ├── screens/       # 页面组件
│   │   └── main.dart      # 应用入口
│   └── pubspec.yaml       # Flutter 依赖配置
└── server/                # Python 后端服务 (FastAPI)
    ├── api/              # API 路由
    ├── services/         # 业务逻辑
    ├── models/           # 数据模型
    ├── main.py           # 服务入口
    └── requirements.txt  # Python 依赖配置
```

## 核心功能

### ✨ 已实现

1. **极简首页**
   - Google 风格单一搜索框
   - 显示最近 1-5 条搜索历史
   - 智能去重（基础版本）

2. **双向翻译查询** ⭐ 新增
   - 中文输入 → 自动翻译为英文 → 返回英文释义 + 中文翻译
   - 英文输入 → 返回英文释义 + 中文翻译
   - 自动语言检测
   - 批量翻译释义和例句

3. **收藏功能** ⭐ 新增
   - 添加/删除收藏
   - 收藏列表管理
   - 检查单词是否已收藏
   - JSON 文件持久化存储

4. **历史记录**
   - 本地存储（SharedPreferences）
   - 点击快速查询
   - 显示合并的相似词变体数量

5. **后端 API** (Python + FastAPI)
   - 双向搜索接口
   - 收藏管理接口
   - 集成 Free Dictionary API
   - 集成 Google Translate

### 🚧 待完善

- 编辑距离算法（Levenshtein Distance）
- NLP 词形还原（Lemmatization）
- 缓存系统（Redis）
- 单元测试
- 更多语言支持

---

## 快速开始

### 前置要求

- **Flutter**: >= 3.0.0
- **Python**: >= 3.8
- **Dart**: >= 3.0.0

### 1. 启动后端服务

```bash
cd server

# 方法 1: 使用启动脚本（推荐）
./run.sh

# 方法 2: 手动启动
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

服务将运行在 `http://localhost:3000`

**访问 API 文档**: http://localhost:3000/docs

测试接口：
```bash
# 健康检查
curl http://localhost:3000/health

# 英文查询
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'

# 中文查询
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'

# 获取收藏列表
curl http://localhost:3000/api/favorites
```

### 2. 运行 Flutter 应用

```bash
cd app

# 安装依赖
flutter pub get

# 运行应用（iOS 模拟器）
flutter run -d ios

# 运行应用（Android 模拟器）
flutter run -d android

# 运行应用（Web）
flutter run -d chrome
```

### 3. 配置 API 地址

如果后端服务地址不是 `localhost:3000`，请修改：

**app/lib/services/api_config.dart**:
```dart
static const String baseUrl = 'http://YOUR_SERVER_IP:3000/api';
```

注意：
- iOS 模拟器使用 `localhost`
- Android 模拟器使用 `10.0.2.2`
- 真机测试使用实际 IP 地址

---

## API 文档

### 自动生成的 API 文档

启动服务后访问: http://localhost:3000/docs

### 1. 搜索接口（双向翻译）

**POST** `/api/search`

**请求体**:
```json
{
  "query": "hello"  // 或 "你好"
}
```

**响应示例** (英文查询):
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
  }
}
```

**响应示例** (中文查询):
```json
{
  "query": "你好",
  "detected_language": "zh-CN",
  "english": "hello",
  "result": {
    "word": "hello",
    "phonetic": "/həˈləʊ/",
    "chinese": "你好",
    "meanings": [...]
  }
}
```

---

### 2. 收藏接口

**添加收藏** - `POST /api/favorites`
```json
{
  "word": "hello",
  "phonetic": "/həˈləʊ/",
  "chinese": "你好"
}
```

**获取收藏列表** - `GET /api/favorites`

**删除收藏** - `DELETE /api/favorites/{id}`

**检查是否已收藏** - `GET /api/favorites/check/{word}`

---

## 开发指南

### 前端架构

**目录说明**:
- `models/`: 数据模型（轻量级手动 JSON 序列化）
- `services/`:
  - `dictionary_service.dart`: API 调用
  - `history_service.dart`: 本地历史记录管理
- `screens/`:
  - `home_screen.dart`: 首页（搜索框 + 历史）
  - `word_detail_screen.dart`: 单词详情页

**状态管理**: 使用 StatefulWidget（轻量级，无额外依赖）

### 后端架构

**技术栈**:
- FastAPI (Python Web 框架)
- Uvicorn (ASGI 服务器)
- httpx (异步 HTTP 客户端)
- googletrans (Google 翻译)
- Pydantic (数据验证)

**服务模块**:
- `dictionary.py`: 调用 Free Dictionary API
- `translation.py`: Google 翻译服务
- `favorites.py`: 收藏管理（JSON 存储）

**API 路由**:
- `search.py`: 搜索接口
- `favorites.py`: 收藏接口

### 添加新功能

1. **前端添加新页面**:
   - 在 `app/lib/screens/` 创建新文件
   - 使用 `Navigator.push()` 导航

2. **后端添加新 API**:
   - 在 `server/api/` 添加路由
   - 在 `server/services/` 实现业务逻辑
   - 在 `main.py` 注册路由

---

## 替代翻译服务

当前使用 `googletrans`（Google Translate 非官方）。如需切换：

### 方案 1: DeepL API（推荐）

**优点**: 翻译质量高，免费额度 500,000 字符/月

```bash
pip install deepl
```

修改 `server/services/translation.py`

### 方案 2: 百度翻译 API

**优点**: 国内速度快，免费额度大

```bash
pip install baidu-trans
```

### 方案 3: LibreTranslate（开源）

**优点**: 开源、可自托管

```bash
pip install libretranslatepy
```

查看 `server/README.md` 了解详细配置。

---

## 生产部署

### 后端部署

**推荐平台**:
- Railway (一键部署)
- Render (免费额度)
- Fly.io (全球分发)
- Vercel (Serverless)

**部署步骤**:
```bash
# 使用 Gunicorn + Uvicorn Workers
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000
```

**Docker 部署**:
```bash
docker build -t air-dict-api .
docker run -p 3000:3000 air-dict-api
```

### 前端部署

**移动端**:
```bash
# Android
flutter build apk --release
# 输出: build/app/outputs/flutter-apk/app-release.apk

# iOS
flutter build ios --release
# 需要 Xcode 签名和发布
```

**Web**:
```bash
flutter build web --release
# 输出: build/web/
# 可部署到 Vercel/Netlify
```

---

## 性能优化建议

1. **前端**:
   - 使用 `const` 构造函数减少重建
   - 图片懒加载
   - 实现虚拟列表（长历史记录）

2. **后端**:
   - 添加 Redis 缓存（词典结果）
   - API 请求限流
   - 压缩响应（Gzip）

3. **网络**:
   - 使用 CDN 加速静态资源
   - 启用 HTTP/2

---

## 常见问题

### Q: Flutter 运行报错 "Waiting for another flutter command to release the startup lock"

**A**: 删除锁文件
```bash
rm /Users/$USER/.flutter/bin/cache/lockfile
```

### Q: Android 模拟器无法连接 localhost

**A**: 使用 `10.0.2.2` 替代 `localhost`
```dart
static const String baseUrl = 'http://10.0.2.2:3000/api';
```

### Q: iOS 报错 "Insecure HTTP is not allowed"

**A**: 在 `ios/Runner/Info.plist` 添加:
```xml
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <true/>
</dict>
```

### Q: 如何清空历史记录？

**A**: 目前需要在代码中调用 `historyService.clearHistory()`，后续可添加 UI 按钮。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

**开发流程**:
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 许可证

MIT License

---

## 鸣谢

- [Free Dictionary API](https://dictionaryapi.dev/) - 免费词典接口
- [Flutter](https://flutter.dev/) - 跨平台 UI 框架
- [FastAPI](https://fastapi.tiangolo.com/) - Python Web 框架
- [googletrans](https://github.com/ssut/py-googletrans) - 翻译服务

---

## 联系方式

如有问题或建议，欢迎提交 Issue。
