from fastapi import APIRouter

# 创建一个 APIRouter 实例
api_router = APIRouter()

# 导入具体的 endpoints
from app.api.v1.endpoints import dialogue, generate, upload

# 包含子路由
api_router.include_router(dialogue.router, prefix="/dialogue", tags=["对话交互"])
api_router.include_router(generate.router, prefix="/generate", tags=["课件生成"])
api_router.include_router(upload.router, prefix="/upload", tags=["文件上传"])

# 暂时保留一个空的路由，防止 main.py 启动时没东西
@api_router.get("/ping")
def ping():
    return {"message": "API Router is active"}