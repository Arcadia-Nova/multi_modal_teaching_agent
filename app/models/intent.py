# app/models/intent.py (或放在 core/intent/schema.py)
from typing import List, Optional
from pydantic import BaseModel


class TeachingIntent(BaseModel):
    subject: Optional[str] = None  # 学科，如"初中物理"
    topic: Optional[str] = None  # 主题，如"欧姆定律"
    key_points: List[str] = []  # 核心知识点列表
    difficult_points: List[str] = []  # 重难点列表
    duration_minutes: Optional[int] = None  # 课堂时长（分钟）
    teaching_style: Optional[str] = None  # 教学风格: "讲授式"/"探究式"/"案例式"
    target_audience: Optional[str] = None  # 目标学段: "初中"/"高中"/"大学"
    special_requirements: List[str] = []  # 特殊要求，如"需要互动游戏"

    # 辅助字段
    is_complete: bool = False  # 是否足够生成课件
    missing_fields: List[str] = []  # 缺失字段列表