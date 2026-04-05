# app/models/courseware.py
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum
import enum
from app.models.common import BaseModel


class CoursewareType(enum.Enum):
    PPT = "ppt"
    WORD = "word"
    GAME = "game"
    ANIMATION = "animation"


class GeneratedCourseware(BaseModel):
    __tablename__ = "generated_courseware"

    session_id = Column(String(64), index=True, nullable=False)
    type = Column(Enum(CoursewareType), nullable=False)
    file_path = Column(String(512), nullable=False)  # 存储路径
    file_name = Column(String(256), nullable=False)  # 下载文件名
    version = Column(Integer, default=1)  # 迭代版本号
    generation_params = Column(JSON)  # 生成时使用的指令集（JSON）
    download_count = Column(Integer, default=0)
    is_latest = Column(Integer, default=1)  # 是否为最新版本（用于迭代）
    expired_at = Column(DateTime, nullable=True)  # 临时文件过期时间


class ModificationRecord(BaseModel):
    __tablename__ = "modification_records"

    session_id = Column(String(64), index=True, nullable=False)
    courseware_id = Column(Integer, index=True, nullable=False)  # 关联 generated_courseware.id
    original_version = Column(Integer, nullable=False)
    new_version = Column(Integer, nullable=False)
    user_request = Column(String(1000), nullable=False)  # 用户原始修改意见
    parsed_modification = Column(JSON)  # 解析后的修改指令（如 {"target":"slide_3","operation":"replace_text"}）
    status = Column(String(20), default="success")  # success, failed

