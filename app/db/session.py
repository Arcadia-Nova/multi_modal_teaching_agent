"""
数据库会话管理
"""
from app.database import engine, Base


def init_db():
    """
    初始化数据库
    
    创建所有表结构
    """
    # 创建所有表结构
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成")
