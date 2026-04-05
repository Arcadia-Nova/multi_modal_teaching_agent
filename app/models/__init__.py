# app/models/__init__.py
from app.models.conversation import ConversationSession, Message, TeachingIntent
from app.models.reference import UploadedFile, ParsedReference, FileType
from app.models.courseware import GeneratedCourseware, ModificationRecord, CoursewareType
from app.models.common import BaseModel

__all__ = [
    "ConversationSession", "Message", "TeachingIntent",
    "UploadedFile", "ParsedReference", "FileType",
    "GeneratedCourseware", "ModificationRecord", "CoursewareType",
    "BaseModel"
]