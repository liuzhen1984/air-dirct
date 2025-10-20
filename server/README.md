# Air Dict 后端服务

基于 FastAPI 的高性能词典 API，支持中英互译、LLM 增强解释和收藏功能。

## 🚀 快速开始

### 启动服务（推荐）

```bash
# 一键启动（自动安装依赖）
./run.sh

# 或手动使用 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

服务运行在 `http://localhost:3000`，API 文档：http://localhost:3000/docs

---

## 📚 核心功能

### 1. 搜索接口（双向翻译）

**POST** `/api/search`

```bash
# 英文查询（~20ms，使用本地 ECDICT 词典）
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'

# 中文查询
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'
```

**性能优化**：
- ⚡ 英文查询：~10-20ms（跳过翻译 API）
- 🚀 并发翻译：使用 `asyncio.gather()` 加速
- 📊 智能翻译：仅翻译 ECDICT 缺失的内容
- 💾 本地词典：77万+ 词汇，离线可用

### 2. LLM 增强解释

**POST** `/api/llm-explain`

```bash
curl -X POST http://localhost:3000/api/llm-explain \
  -H "Content-Type: application/json" \
  -d '{"word": "serendipity"}'
```

提供：详细解释、词源、记忆技巧、例句、近反义词等

**配置**：在 `.env` 设置 `OPENAI_API_KEY`

### 3. 收藏管理

```bash
# 添加收藏
POST /api/favorites

# 获取列表
GET /api/favorites

# 删除收藏
DELETE /api/favorites/{id}

# 检查是否已收藏
GET /api/favorites/check/{word}
```

---

## 🔧 技术栈

- **FastAPI** - 现代 Python Web 框架
- **ECDICT** - 本地词典（77万+ 词汇）
- **deep-translator** - Google 翻译（并发优化）
- **OpenAI API** - LLM 增强解释
- **uv** - 快速依赖管理

---

## 📁 项目结构

```
server/
├── main.py              # 应用入口
├── api/                 # API 路由
│   ├── search.py        # 搜索接口（已优化）
│   ├── favorites.py     # 收藏管理
│   └── llm.py          # LLM 增强
├── services/            # 业务逻辑
│   ├── dictionary.py    # 本地词典（ECDICT）
│   ├── translation.py   # 翻译服务（并发）
│   └── llm_service.py   # LLM 服务
├── models/              # 数据模型
└── data/
    ├── dict/
    │   └── stardict.db  # ECDICT 数据库
    └── favorites.json   # 收藏记录
```

---

## ⚙️ 配置说明

### 环境变量（.env）

```bash
# 服务端口（可选，默认 3000）
PORT=3000

# OpenAI API（LLM 增强功能）
OPENAI_API_KEY=sk-xxx...
OPENAI_MODEL=gpt-4o-mini  # 推荐：性价比高
```

---

## 🎯 性能优化详解

### 优化前后对比

| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 英文查询 | ~2-3秒 | <0.02秒 | **100-150倍** |
| 中文查询 | ~3-4秒 | ~0.23秒 | **13-17倍** |
| 复杂单词 | ~4-5秒 | <0.02秒 | **200-250倍** |

### 主要优化技术

1. **本地词典优先**：使用 ECDICT，避免网络调用
2. **并发翻译**：`asyncio.gather()` 同时处理多个请求
3. **智能缓存**：利用 ECDICT 自带中文翻译
4. **非阻塞 I/O**：线程池执行同步操作

详见：`api/search.py:49-130`（智能翻译逻辑）

---

## 📖 词典对比

| 特性 | ECDICT (本地) | LLM 增强 |
|------|--------------|----------|
| 速度 | ⚡ 1-5ms | 🐌 2-5秒 |
| 成本 | 💰 免费 | 💰 ~$0.0003/次 |
| 离线 | ✅ 完全离线 | ❌ 需要网络 |
| 词汇量 | ✅ 77万+ | ✅ 无限 |
| 解释质量 | ⚠️ 基础 | ✅ 详细、智能 |
| 词源/例句 | ❌ 有限 | ✅ 丰富 |

**推荐策略**：快速查词用本地，深度学习用 LLM

---

## 🐛 常见问题

### Q: 翻译服务慢？
**A**: 已优化！使用本地 ECDICT 词典，英文查询 <20ms

### Q: ECDICT 数据库在哪？
**A**: `data/dict/stardict.db`（自动下载）

### Q: 如何启用 LLM 增强？
**A**: 在 `.env` 设置 `OPENAI_API_KEY`

### Q: 端口被占用？
**A**: 修改 `.env` 中的 `PORT` 或运行 `uvicorn main:app --port 8000`

---

## 🚀 部署

### Docker

```bash
docker build -t air-dict-api .
docker run -p 3000:3000 air-dict-api
```

### 生产环境

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4
```

推荐平台：Railway、Render、Fly.io

---

## 📝 许可证

MIT License

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [ECDICT](https://github.com/skywind3000/ECDICT) - 开源词典
- [deep-translator](https://github.com/nidhaloff/deep-translator)
