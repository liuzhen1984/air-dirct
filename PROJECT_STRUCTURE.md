# 项目文件结构

```
air-dirct/
│
├── DESIGN.md                          # 详细设计文档
├── README.md                          # 项目总览和快速开始
├── PROJECT_STRUCTURE.md               # 本文件
│
├── app/                               # Flutter 前端应用
│   ├── README.md                      # 前端文档
│   ├── pubspec.yaml                   # Flutter 依赖配置
│   ├── analysis_options.yaml          # Dart 代码规范
│   ├── .gitignore                     # Git 忽略文件
│   │
│   └── lib/
│       ├── main.dart                  # 应用入口
│       │
│       ├── models/                    # 数据模型层
│       │   ├── word_definition.dart   # 单词释义模型
│       │   ├── word_definition.g.dart # JSON 序列化代码（生成）
│       │   ├── history_item.dart      # 历史记录模型
│       │   └── history_item.g.dart    # JSON 序列化代码（生成）
│       │
│       ├── services/                  # 服务层（API 调用 + 本地存储）
│       │   ├── api_config.dart        # API 配置（URL、超时等）
│       │   ├── dictionary_service.dart # 词典 API 服务
│       │   └── history_service.dart   # 历史记录服务
│       │
│       ├── screens/                   # 页面层
│       │   ├── home_screen.dart       # 首页（搜索框 + 历史记录）
│       │   └── word_detail_screen.dart # 单词详情页
│       │
│       └── widgets/                   # 可复用组件（预留）
│
└── server/                            # Node.js 后端服务
    ├── README.md                      # 后端文档
    ├── package.json                   # Node.js 依赖配置
    ├── .env.example                   # 环境变量示例
    ├── .gitignore                     # Git 忽略文件
    │
    └── src/
        ├── index.js                   # 服务入口（Express 服务器）
        │
        ├── routes/                    # API 路由层
        │   └── search.js              # 搜索相关路由
        │
        ├── services/                  # 业务逻辑层
        │   ├── dictionaryService.js   # 词典服务（调用第三方 API）
        │   └── translationService.js  # 翻译服务（语言检测 + 翻译）
        │
        └── utils/                     # 工具函数（预留）
```

## 文件说明

### 前端核心文件

| 文件 | 说明 | 关键功能 |
|------|------|----------|
| `main.dart` | 应用入口 | 初始化 SharedPreferences，启动应用 |
| `home_screen.dart` | 首页 | 搜索框、历史记录展示、导航 |
| `word_detail_screen.dart` | 详情页 | 调用 API、展示释义、错误处理 |
| `dictionary_service.dart` | API 客户端 | HTTP 请求、超时处理、异常封装 |
| `history_service.dart` | 历史管理 | 本地存储、智能去重、CRUD 操作 |
| `api_config.dart` | API 配置 | 服务器地址、超时时间、端点定义 |

### 后端核心文件

| 文件 | 说明 | 关键功能 |
|------|------|----------|
| `index.js` | 服务入口 | Express 配置、路由注册、错误处理 |
| `search.js` | API 路由 | `/search`, `/definition`, `/translate` |
| `dictionaryService.js` | 词典服务 | 调用 Free Dictionary API，数据转换 |
| `translationService.js` | 翻译服务 | 语言检测、翻译（当前 Mock） |

## 数据流

```
用户输入 "hello"
    ↓
[HomeScreen] 搜索框 onSubmitted
    ↓
[HistoryService] 添加到历史记录（智能去重）
    ↓
[Navigator] 跳转到 WordDetailScreen
    ↓
[DictionaryService] HTTP POST /api/search
    ↓
[Server: search.js] 接收请求
    ↓
[TranslationService] 检测语言 → 英文
    ↓
[DictionaryService] 调用 Free Dictionary API
    ↓
[Server] 返回 JSON 响应
    ↓
[WordDetailScreen] 展示释义
```

## 配置文件

### `pubspec.yaml`
Flutter 依赖管理，定义：
- SDK 版本
- 第三方包（http, shared_preferences, provider）
- 资源文件（图片、字体等）

### `package.json`
Node.js 依赖管理，定义：
- 脚本命令（start, dev）
- 依赖包（express, axios, cors）

### `.env`
环境变量配置（需从 `.env.example` 复制）：
- `PORT`: 服务器端口
- `NODE_ENV`: 运行环境
- 第三方 API Key（可选）

## 扩展指南

### 添加新页面（前端）

1. 在 `lib/screens/` 创建新文件
2. 使用 `Navigator.push()` 导航
3. 可选：添加到 `MaterialApp` 的 `routes`

### 添加新 API（后端）

1. 在 `src/services/` 创建业务逻辑
2. 在 `src/routes/` 创建路由
3. 在 `src/index.js` 注册路由

### 集成数据库

建议添加以下目录：
```
server/src/
├── models/       # 数据库模型（Mongoose/Sequelize）
├── config/       # 数据库配置
└── middleware/   # 认证、日志等中间件
```

### 添加用户系统

1. 前端添加 `lib/services/auth_service.dart`
2. 后端添加 `src/routes/auth.js` 和 JWT 中间件
3. 使用 Provider 管理用户状态

## 待办事项

查看 `DESIGN.md` 的 "实现路线图" 部分了解详细的开发计划。

### 高优先级
- [ ] 集成真实翻译 API
- [ ] 实现编辑距离算法
- [ ] 添加缓存系统（Redis）

### 中优先级
- [ ] 添加单元测试
- [ ] 实现搜索建议（自动完成）
- [ ] 深色模式

### 低优先级
- [ ] PWA 支持
- [ ] 用户账户系统
- [ ] 导出历史记录

## 开发建议

1. **前端开发**：使用 `flutter run -d chrome` 在浏览器中快速调试
2. **后端开发**：使用 `npm run dev` 启用热重载
3. **API 测试**：使用 Postman 或 curl 测试后端接口
4. **调试**：使用 Chrome DevTools（Flutter Web）或 Xcode/Android Studio（移动端）

## 性能优化

- 前端：使用 `const` 构造函数，避免不必要的重建
- 后端：添加缓存层（Redis），减少 API 调用
- 网络：压缩响应体，启用 HTTP/2
