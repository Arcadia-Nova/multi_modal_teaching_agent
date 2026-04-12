<<<<<<< Updated upstream
=======
from fastapi import Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db

def get_session_id(
    request: Request,
    x_session_id: Optional[str] = Header(None)
) -> str:
    """
    从请求头 X-Session-ID 获取会话ID，如果没有则创建新的（由服务层负责创建）。
    此处仅提取并返回，若不存在则返回 None 或抛出异常，服务层会处理。
    """
    if x_session_id:
        return x_session_id
    # 也可以从查询参数获取
    session_id = request.query_params.get("session_id")
    if session_id:
        return session_id
    raise HTTPException(status_code=400, detail="缺少 session_id，请提供 X-Session-ID 头或 query 参数 session_id")

# 数据库会话依赖
def get_db_session() -> Session:
    return next(get_db())
>>>>>>> Stashed changes
