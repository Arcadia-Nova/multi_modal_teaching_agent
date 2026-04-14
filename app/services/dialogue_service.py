# app/services/dialogue_service.py
from typing import Dict, List, Optional, Any, AsyncGenerator

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.intent.extractor import IntentExtractor
from app.core.intent.clarifier import Clarifier
from app.models.conversation import Message, TeachingIntent
from app.services.message_service import MessageService

class DialogueService:
    def __init__(self,db: Session ,llm_client):
        self.db = db
        self.extractor = IntentExtractor(llm_client)
        self.llm_client = llm_client
        self.clarifier = Clarifier()
        self.message_service = MessageService(db)
        # 会话存储：session_id -> {history, current_intent}
        self.sessions: Dict[str, Dict] = {}
        # 用于缓存流式输出的完整内容
        # 结构: session_id -> "完整回复文本"
        self.stream_cache: Dict[str, str] = {}

    def process_message(self, session_id: str, user_message: str) -> str:
        """处理教师消息，返回助手回复"""
        # 获取或创建会话
        if session_id not in self.sessions:
            self.sessions[session_id] = {"history": [], "intent": TeachingIntent()}
        session = self.sessions[session_id]

        # 添加用户消息到历史
        self.message_service.save_message(session_id, "user", user_message)

        history = self.message_service.get_history(session_id)

        # 提取当前意图（基于全部历史）
        updated_intent = self.extractor.extract(history)
        session["intent"] = updated_intent

        # 判断是否完整
        if updated_intent.is_complete:
            # 生成确认信息
            summary = self.clarifier.generate_summary(updated_intent)
            self._save_intent(session_id, updated_intent)
            reply = f"已理解您的教学需求：\n{summary}\n\n如果确认无误，请回复“确认生成”开始制作课件；如需修改，请直接告诉我。"
        else:
            # 生成追问
            questions = self.clarifier.generate_questions(updated_intent)
            if questions:
                reply = questions[0]  # 一次问一个
            else:
                reply = "请提供更多教学信息（如学科、主题、知识点等）。"

        # 添加助手回复到历史
        self.message_service.save_message(session_id, "assistant", reply)
        return reply

    def confirm_and_get_intent(self, session_id: str) -> TeachingIntent:
        """教师确认后，返回最终意图（供生成模块使用）"""
        session = self.sessions.get(session_id)
        if session and session["intent"].is_complete:
            return session["intent"]
        raise ValueError("意图未完整，无法生成课件")

    def _save_intent(self, session_id: str, intent: 'TeachingIntent'):
        """保存或更新教学意图（每次提取都存新记录）"""
        record = TeachingIntent(
            session_id=session_id,
            subject=intent.subject,
            topic=intent.topic,
            key_points=intent.key_points,
            difficult_points=intent.difficult_points,
            duration_minutes=intent.duration_minutes,
            teaching_style=intent.teaching_style,
            target_audience=intent.target_audience,
            special_requirements=intent.special_requirements,
            raw_intent_json=intent.dict()
        )

        existing = self.db.query(TeachingIntent).filter(TeachingIntent.session_id == session_id).first()
        if existing:
            # 更新现有记录
            for key, value in intent.dict().items():
                setattr(existing, key, value)
            existing.updated_at = func.now()
        else:
            # 创建新记录
            self.db.add(record)
        self.db.commit()


    def get_intent_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取当前会话的最新教学意图（结构化）"""
        intent_record = self.db.query(TeachingIntent).filter(
            TeachingIntent.session_id == session_id
        ).order_by(TeachingIntent.id.desc()).first()
        if not intent_record:
            return None
        # 转换为字典，排除内部字段
        return {
            "subject": intent_record.subject,
            "topic": intent_record.topic,
            "key_points": intent_record.key_points,
            "difficult_points": intent_record.difficult_points,
            "duration_minutes": intent_record.duration_minutes,
            "teaching_style": intent_record.teaching_style,
            "target_audience": intent_record.target_audience,
            "special_requirements": intent_record.special_requirements
        }


    def get_history(self, session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """获取会话的对话历史，返回格式 [{"role": "user/assistant", "content": "..."}]"""
        messages = self.db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at).limit(limit).all()
        # return [{"role": msg.role, "content": msg.content} for msg in messages]
        return messages

    async def chat_stream(self, session_id: str, user_message: str) -> AsyncGenerator[str, None]:
        """
        通用对话流式接口（异步）
        """
        # 1. 保存用户消息
        self.message_service.save_message(session_id, "user", user_message)

        # 2. 获取历史记录并构建 Messages
        history_messages = self.message_service.get_history(session_id)
        if history_messages:
            messages = history_messages

        # 3. 初始化缓存
        self.stream_cache[session_id] = ""

        try:
            # 4. 调用 LLMClient 的 astream 接口
            # 注意：这里使用 async for 遍历异步生成器
            async for chunk in self.llm_client.astream(messages=messages):
                # chunk 是 LLMClient 返回的 delta 内容（字符串）
                self.stream_cache[session_id] += chunk
                yield chunk

        except Exception as e:
            error_msg = f"AI 回复出错: {str(e)}"
            for char in error_msg:
                yield char

        # 5. 流式结束后，保存完整回复到数据库
        final_text = self.stream_cache.get(session_id, "")
        if final_text:
            self.message_service.save_message(session_id, "assistant", final_text)
            # 清理缓存
            self.stream_cache.pop(session_id, None)

