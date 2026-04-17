# app/services/session_service.py
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.conversation import ConversationSession

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_name: str = None) -> str:
        """创建新会话，返回 session_id"""
        session_id = str(uuid.uuid4())
        session = ConversationSession(
            session_id=session_id,
            user_name=user_name,
            last_active=datetime.now(),
            status="active"
        )
        self.db.add(session)
        self.db.commit()
        return session_id

    def get_session(self, session_id: str) -> ConversationSession:
        """获取会话记录，若不存在则返回 None"""
        return self.db.query(ConversationSession).filter(
            ConversationSession.session_id == session_id
        ).first()

    def update_last_active(self, session_id: str):
        """更新最后活动时间"""
        session = self.get_session(session_id)
        if session:
            session.last_active = datetime.now()
            self.db.commit()

    def get_all_session(self):
        return self.db.query(ConversationSession).order_by(ConversationSession.created_at.desc()).all()