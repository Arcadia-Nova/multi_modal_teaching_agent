# app/models/conversation.py
from sqlalchemy import Column, String, DateTime, JSON, Integer
from app.models.common import BaseModel


class ConversationSession(BaseModel):
    __tablename__ = "conversation_sessions"

    session_id = Column(String(64), unique=True, index=True, nullable=False)  # UUID
    user_name = Column(String(128), nullable=True)  # 可选，教师姓名
    last_active = Column(DateTime, nullable=False)  # 最后活动时间
    status = Column(String(20), default="active")  # active, expired, archived
    metadata_json = Column(JSON, default=dict)  # 扩展信息（如前端设置）


class Message(BaseModel):
    __tablename__ = "messages"

    session_id = Column(String(64), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(String(2000), nullable=False)  # 文本内容
    raw_audio_path = Column(String(512), nullable=True)  # 若为语音输入，存储原始文件路径


class TeachingIntent(BaseModel):
    __tablename__ = "teaching_intents"

    session_id = Column(String(64), index=True, unique=True, nullable=False)
    subject = Column(String(100))  # 学科
    topic = Column(String(200))  # 主题
    key_points = Column(JSON)  # 知识点列表，如 ["欧姆定律", "电阻"]
    difficult_points = Column(JSON)  # 重难点列表
    duration_minutes = Column(Integer)  # 时长（分钟）
    teaching_style = Column(String(50))  # 讲授式/探究式/案例式
    target_audience = Column(String(50))  # 初中/高中/大学
    special_requirements = Column(JSON)  # 其他要求，如 {"need_game": true}
    raw_intent_json = Column(JSON)  # 保留原始大模型输出