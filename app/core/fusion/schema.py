# app/core/fusion/schema.py
from typing import List, Dict, Optional
from pydantic import BaseModel

class ReferenceFragment(BaseModel):
    file_id: str
    file_name: str
    content_type: str   # "text", "ocr", "image_desc", "video_summary"
    content: str        # 实际文本片段
    reference_note: Optional[str] = None  # 教师标注，如“参考第3页案例”
    metadata: Dict = {}  # 页码、时间戳等

class RetrievalFragment(BaseModel):
    source: str          # 来源文件
    content: str         # 检索到的文本块
    score: float

class FusionContext(BaseModel):
    intent: dict         # 结构化教学意图（来自IntentExtractor）
    references: List[ReferenceFragment]   # 解析后的参考资料摘要
    retrieval: List[RetrievalFragment]    # RAG检索结果