from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from api import search_router, favorites_router, llm_router

# 加载环境变量
load_dotenv()

# 创建 FastAPI 应用
app = FastAPI(
    title="Air Dict API",
    description="轻量级英文词典 API - 双向翻译 + 收藏功能 + LLM 增强",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(search_router)
app.include_router(favorites_router)
app.include_router(llm_router)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "Air Dict API is running",
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Air Dict API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "search": "POST /api/search",
            "definition": "GET /api/definition/{word}",
            "llm": {
                "explain": "POST /api/llm-explain",
                "explain_get": "GET /api/llm-explain/{word}",
            },
            "favorites": {
                "list": "GET /api/favorites",
                "add": "POST /api/favorites",
                "delete": "DELETE /api/favorites/{id}",
                "check": "GET /api/favorites/check/{word}",
            },
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "True").lower() == "true"

    print(f"\n🚀 Starting Air Dict API Server...")
    print(f"📖 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🏥 Health Check: http://localhost:{port}/health\n")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
    )
