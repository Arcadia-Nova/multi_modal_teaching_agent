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

class GameContentItem(BaseModel):
    """游戏内容项"""
    title: str = Field(..., description="游戏题目")
    content: List[str] = Field(..., description="游戏选项或内容")

class GeneratePPTRequest(BaseModel):
    """生成PPT请求"""
    topic: str = Field(..., description="PPT主题")
    content: Optional[List[PPTContentItem]] = Field(None, description="PPT内容")
    outline: Optional[PPTOutline] = Field(None, description="PPT大纲")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateGameRequest(BaseModel):
    """生成游戏请求"""
    topic: str = Field(..., description="游戏主题")
    content: Optional[List[GameContentItem]] = Field(None, description="游戏内容")
    game_type: str = Field("quiz", description="游戏类型 (quiz, memory, matching)")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateCoursewareRequest(BaseModel):
    """生成课件请求"""
    topic: str = Field(..., description="课件主题")
    type: str = Field(..., description="课件类型 (ppt, word, animation, game)")
    content: Optional[List[PPTContentItem]] = Field(None, description="课件内容")
    outline: Optional[PPTOutline] = Field(None, description="课件大纲")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GeneratePPTWithAIRequest(BaseModel):
    """使用AI生成PPT请求"""
    topic: str = Field(..., description="PPT主题")
    requirements: Optional[str] = Field(None, description="自定义要求")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class EnhancePPTWithAIRequest(BaseModel):
    """使用AI增强PPT内容请求"""
    topic: str = Field(..., description="PPT主题")
    content: List[PPTContentItem] = Field(..., description="PPT内容")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateLessonPlanWithAIRequest(BaseModel):
    """使用AI生成教案请求"""
    topic: str = Field(..., description="教案主题")
    requirements: Optional[str] = Field(None, description="自定义要求")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateLessonPlanFromPPTWithAIRequest(BaseModel):
    """从PPT内容生成AI增强教案请求"""
    topic: str = Field(..., description="教案主题")
    ppt_content: List[PPTContentItem] = Field(..., description="PPT内容")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateGameWithAIRequest(BaseModel):
    """使用AI生成游戏请求"""
    topic: str = Field(..., description="游戏主题")
    game_type: str = Field("quiz", description="游戏类型 (quiz, memory, matching)")
    requirements: Optional[str] = Field(None, description="自定义要求")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class EnhanceGameWithAIRequest(BaseModel):
    """使用AI增强游戏内容请求"""
    topic: str = Field(..., description="游戏主题")
    content: List[GameContentItem] = Field(..., description="游戏内容")
    game_type: str = Field("quiz", description="游戏类型")
    output_filename: Optional[str] = Field(None, description="输出文件名")

class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
