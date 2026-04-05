# app/models/reference.py
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum
import enum
from app.models.common import BaseModel


class FileType(enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"


class UploadedFile(BaseModel):
    __tablename__ = "uploaded_files"

    session_id = Column(String(64), index=True, nullable=False)
    file_id = Column(String(64), unique=True, index=True, nullable=False)  # UUID
    original_name = Column(String(256), nullable=False)
    file_path = Column(String(512), nullable=False)  # 服务器存储路径
    file_type = Column(Enum(FileType), nullable=False)
    file_size = Column(Integer)  # 字节
    reference_note = Column(String(500))  # 教师标注的参考说明（如“参考第3页案例”）
    parsed_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    uploaded_at = Column(DateTime, nullable=False)


class ParsedReference(BaseModel):
    __tablename__ = "parsed_references"

    file_id = Column(String(64), index=True, nullable=False)
    content_type = Column(String(30), nullable=False)  # text, ocr, image_description, video_frames
    content = Column(String(2000), nullable=False)  # 提取的文本或描述
    metadata_json = Column(JSON)  # 如页码、时间戳、帧序号
    is_summary = Column(Integer, default=0)  # 是否为摘要（1=是）