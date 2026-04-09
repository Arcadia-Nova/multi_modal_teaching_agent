from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PPTContentItem(BaseModel):
    """PPT内容项"""
    title: str = Field(..., description="幻灯片标题")
    content: List[str] = Field(..., description="幻灯片内容列表")

class PPTOutlineSection(BaseModel):
    """PPT大纲章节"""
    title: str = Field(..., description="章节标题")
    content: List[str] = Field(..., description="章节内容")

class PPTOutline(BaseModel):
    """PPT大纲"""
    topic: str = Field(..., description="PPT主题")
    sections: List[PPTOutlineSection] = Field(..., description="PPT章节列表")

class GeneratePPTRequest(BaseModel):
    """生成PPT请求"""
    topic: str = Field(..., description="PPT主题")
    content: Optional[List[PPTContentItem]] = Field(None, description="PPT内容")
    outline: Optional[PPTOutline] = Field(None, description="PPT大纲")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateCoursewareRequest(BaseModel):
    """生成课件请求"""
    topic: str = Field(..., description="课件主题")
    type: str = Field(..., description="课件类型 (ppt, word, animation)")
    content: Optional[List[PPTContentItem]] = Field(None, description="课件内容")
    outline: Optional[PPTOutline] = Field(None, description="课件大纲")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
