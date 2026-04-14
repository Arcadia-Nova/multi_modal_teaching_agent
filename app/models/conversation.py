"""
对话相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Message(Base):
    """
    消息模型
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    sender = Column(String(50), nullable=False)  # 'user' 或 'system'
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    
    conversation = relationship("Conversation", back_populates="messages")


class Conversation(Base):
    """
    对话模型
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="conversation")


class TeachingIntent(Base):
    """
    教学意图模型
    """
    __tablename__ = "teaching_intents"
    
    id = Column(Integer, primary_key=True, index=True)
    intent_type = Column(String(100), nullable=False)
    topic = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConversationSession(Base):
    """
    会话会话模型
    """
    __tablename__ = "conversation_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
