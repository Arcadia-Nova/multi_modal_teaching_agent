# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# SQLite 数据库文件路径（可配置）
DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}" if hasattr(settings, 'DATABASE_PATH') else "sqlite:///./teaching_agent.db"

# 创建引擎，启用外键约束（SQLite 默认关闭）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # 仅 SQLite 需要，允许多线程
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """创建所有表（首次运行时调用）"""
    Base.metadata.create_all(bind=engine)