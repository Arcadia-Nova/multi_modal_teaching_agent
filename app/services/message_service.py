"""
对话记录服务：专门负责处理 Message 模型的数据库读写操作
确保对话历史在数据库中持久化，即使服务重启也不会丢失。
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict

# 假设你的 Message 模型定义在 models/conversation.py 中
from app.models.conversation import Message
from app.models.reference import ParsedReference,UploadedFile


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, session_id: str, role: str, content: str) -> Message:
        """
        保存一条消息到数据库

        Args:
            session_id: 会话ID
            role: 角色 ('user' 或 'assistant')
            content: 消息内容

        Returns:
            保存后的 Message 对象
        """
        db_message = Message(
            session_id=session_id,
            role=role,
            content=content
            # created_at 会自动使用数据库默认值（或在模型中定义的默认值）
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)  # 刷新以获取数据库生成的 ID 等信息
        return db_message

    def get_history(self, session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """
        从数据库获取指定会话的对话历史

        Args:
            session_id: 会话ID
            limit: 限制获取的消息数量

        Returns:
            包含 role 和 content 的字典列表
        """
        query = self.db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at.asc())  # 按时间顺序排列

        if limit:
            query = query.limit(limit)

        messages = query.all()

        # 转换为字典格式，兼容前端或对话逻辑
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    def delete_session_history(self, session_id: str):
        """
        删除某个会话的所有历史记录（可选功能，用于清理）
        """
        self.db.query(Message).filter(Message.session_id == session_id).delete()
        self.db.commit()

    def get_references(self,session_id: str, limit: int = 5) -> List[Dict[str, str]]:
        query = self.db.query(UploadedFile).filter(
            UploadedFile.session_id == session_id
        ).order_by(UploadedFile.created_at.desc())

        if limit:
            query = query.limit(limit)

        reference = query.all()
        ref_list = []
        count = 0

        for ref in reference:
            count += 1
            file_id = ref.file_id
            query_ref = self.db.query(ParsedReference).filter(
                ParsedReference.file_id == file_id
            ).order_by(ParsedReference.created_at.desc())

            reference2 = query_ref.first()
            if reference2:
               ref_list = ref_list + [reference2.content]




        role = str("user")
        des = str("这是用户上传的文档的分析,请进行解析:")

        return [
            { "role": role ,"content": des+ref_list[i]}
            for i in range(len(ref_list))
        ]
