import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router  # 稍后我们会创建这个路由文件
from app.config import settings
from app.core.rag import build_knowledge_base_incremental
from app.db.session import init_db

# --- 应用启动时 同步 构建知识库 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not os.path.exists(settings.VECTOR_DB_PATH) or not os.listdir(settings.VECTOR_DB_PATH):
        print("构建本地知识库...")
        await asyncio.to_thread(build_knowledge_base_incremental())

    init_db()

    yield
    # Shutdown (如果有需要清理的资源，如数据库连接池等)
    print("应用关闭")

# --- 初始化 FastAPI 应用实例 ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## 多模态 AI 互动式教学智能体 API 文档

    本项目旨在为教师提供智能化的教学辅助，核心功能包括：
    - **多模态输入**：支持语音、文本、PDF/视频上传。
    - **智能 RAG**：基于本地知识库的检索增强生成。
    - **课件生成**：自动生成 PPT、Word 教案及互动游戏。
    """,
    version=settings.VERSION,
    docs_url="/docs",  # 访问 http://127.0.0.1:8000/docs 查看文档
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# ---  配置 CORS (跨域资源共享) ---
# 允许前端（如 localhost:3000）调用后端接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议改为具体的域名 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法 (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# ---  挂载静态文件目录 ---
# 用于让前端直接访问生成的 PPT/Word 文件（预览或下载用）
# 访问路径示例: http://127.0.0.1:8000/static/exports/test.pptx
app.mount("/static", StaticFiles(directory=settings.EXPORT_DIR), name="static")


# ---  注册全局异常处理器 ---
# 统一的错误返回格式，方便前端处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 这里可以接入日志系统，记录错误堆栈
    print(f"全局异常捕获: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": str(exc) if settings.DEBUG else "请稍后重试"  # 生产环境不暴露具体错误信息
        }
    )


# ---  注册业务路由 ---
# 将 v1 版本的所有接口挂载到 API_V1_STR 前缀下
app.include_router(api_router, prefix=settings.API_V1_STR)


# ---  根路径健康检查 ---
@app.get("/", tags=["Root"])
async def root():
    """
    根路径检查，确认服务是否启动
    """
    return {
        "message": "欢迎使用多模态 AI 教学智能体",
        "docs": "/docs",
        "status": "Running"
    }


# --- 启动入口 ---
# 只有当直接运行此文件时才启动服务器
if __name__ == "__main__":
    print(f"🚀 正在启动服务: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 查看文档: http://{settings.HOST}:{settings.PORT}/docs")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # 开发模式下开启热重载
        workers=1  # Windows 下多进程可能导致端口占用，建议设为 1
    )