import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    项目全局配置类
    自动读取 .env 文件中的环境变量
    """

    # --- 应用基础配置 ---
    PROJECT_NAME: str = "MultiModal Teaching Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True  # 开发环境设为 True

    # --- 服务器配置 ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- 大模型配置 (LLM) ---
    # 推荐使用 Qwen-72B 或 GLM-4，这里配置 API Key 或 本地路径
    LLM_PROVIDER: str = "dashscope"  # 可选: openai, dashscope (阿里), zhipu (智谱), local
    LLM_API_KEY: str = "sk-2ea33be7c2604c3c8fc17aedfb7d8145"
    LLM_BASE_URL: Optional[str] = None  # 如果部署在本地 vLLM，填 http://localhost:8000/v1
    LLM_MODEL_NAME: str = "qwen-turbo"  # 默认模型

    #--- 语音识别配置 ---
    DASHSCOPE_API_KEY: str = "sk-2ea33be7c2604c3c8fc17aedfb7d8145"

    #--- 视频处理 ---
    VIDEO_FRAME_INTERVAL_SEC: int = 3   # 抽帧间隔（秒）
    MAX_VIDEO_FRAMES: int = 50          # 最多抽取多少帧，避免过多

    # --- 向量数据库配置 (RAG) ---
    VECTOR_DB_TYPE: str = "chroma"  # 可选: chroma, milvus, faiss
    VECTOR_DB_PATH: str = "./vector_store"  # 本地持久化路径
    EMBEDDING_MODEL: str = "BAAI/bge-large-zh-v1.5"  # 中文效果最好的开源 Embedding
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    TOP_K_RETRIEVAL: int = 5

    # --- 本地知识库路径 ---
    KNOWLEDGE_BASE_DIR: str = "../../knowledge_base/documents"
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-large-zh-v1.5"

    #--- 向量库路径 ---
    VECTOR_STORE_PATH: str = "../../../vector_store"

    # --- 文件存储配置 ---
    UPLOAD_DIR: str = "./uploads"
    EXPORT_DIR: str = "./app/static/exports"  # 对应 static 目录
    # 允许上传的文件后缀
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".pptx", ".txt", ".mp4", ".jpg", ".png"]

    # --- 数据库配置 (可选，用于保存历史记录) ---
    # DATABASE_URL: str = "sqlite:///./teaching_agent.db"  # 默认使用 SQLite
    DATABASE_PATH: str = "./teaching_agent.db"

    # --- 安全配置 ---
    SECRET_KEY: str = "your-secret-key-change-this-in-production"

    # --- 模型加载配置 (针对本地部署) ---
    # 如果是本地加载 Qwen-72B，需要指定模型路径
    LOCAL_MODEL_PATH: Optional[str] = None

    # 指定 .env 文件路径
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # 环境变量不区分大小写
    )


# 实例化配置对象
settings = Settings()

# --- 自动创建必要的目录 ---
# 这一步很重要，防止程序启动时因为目录不存在而报错
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.EXPORT_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_BASE_DIR, exist_ok=True)

# 计算基于项目根目录的绝对路径（派生路径，不作为配置字段）
BASE_DIR = Path(__file__).resolve().parent.parent  # 项目根目录
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base" / "documents"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"
# 如果 settings 中的路径是相对路径，则转换为绝对路径
settings.KNOWLEDGE_BASE_DIR = str(KNOWLEDGE_BASE_DIR)
settings.VECTOR_STORE_PATH = str(VECTOR_STORE_PATH)
if not os.path.isabs(settings.UPLOAD_DIR):
    settings.UPLOAD_DIR = str(BASE_DIR / settings.UPLOAD_DIR)
if not os.path.isabs(settings.DATABASE_PATH):
    settings.DATABASE_PATH = str(BASE_DIR / settings.DATABASE_PATH)