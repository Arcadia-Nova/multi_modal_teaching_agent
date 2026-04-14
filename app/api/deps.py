"""
API 依赖项
"""
from sqlalchemy.orm import Session
from fastapi import Cookie, HTTPException
from app.database import get_db
import uuid


def get_db_session():
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def get_session_id(session_id: str = Cookie(None)):
    """
    获取会话 ID
    
    Args:
        session_id: 会话 ID
        
    Returns:
        str: 会话 ID
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id
