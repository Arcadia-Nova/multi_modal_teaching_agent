# app/db/base.py
from app.db.session import Base  # 实际定义在 session.py 中
# from app.models.common import BaseModel
# from app.models.conversation import ConversationSession, Message, TeachingIntent
# from app.models.reference import UploadedFile, ParsedReference
# from app.models.courseware import GeneratedCourseware, ModificationRecord

# 确保所有模型被导入，Alembic 才能自动检测
# __all__ = ["Base", "ConversationSession", "Message", "TeachingIntent",
#            "UploadedFile", "ParsedReference", "GeneratedCourseware", "ModificationRecord"]