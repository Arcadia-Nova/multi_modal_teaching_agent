from fastapi import APIRouter, HTTPException
from app.api.v1.models.generate import (
    GeneratePPTRequest, 
    GenerateCoursewareRequest, 
    GenerateResponse,
    GenerateGameRequest,
    GeneratePPTWithAIRequest,
    EnhancePPTWithAIRequest,
    GenerateLessonPlanWithAIRequest,
    GenerateLessonPlanFromPPTWithAIRequest,
    GenerateGameWithAIRequest,
    EnhanceGameWithAIRequest
)
from app.services.generation_service import GenerationService

router = APIRouter()
generation_service = GenerationService()

@router.post("/ppt", response_model=GenerateResponse, summary="生成PPT")
async def generate_ppt(request: GeneratePPTRequest):
    """
    生成PPT
    
    - **topic**: PPT主题
    - **content**: PPT内容（可选）
    - **outline**: PPT大纲（可选）
    - **output_filename**: 输出文件名（可选）
    
    如果既没有提供content也没有提供outline，将使用LLM自动生成大纲
    """
    try:
        # 转换请求数据为服务所需格式
        content = None
        if request.content:
            content = [item.model_dump() for item in request.content]
        
        outline = None
        if request.outline:
            outline = request.outline.model_dump()
        
        # 调用生成服务
        result = generation_service.generate_ppt(
            topic=request.topic,
            content=content,
            outline=outline,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成PPT失败: {str(e)}")

@router.post("/game", response_model=GenerateResponse, summary="生成游戏")
async def generate_game(request: GenerateGameRequest):
    """
    生成游戏
    
    - **topic**: 游戏主题
    - **content**: 游戏内容（可选）
    - **game_type**: 游戏类型 (quiz, memory, matching)
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 转换请求数据为服务所需格式
        content = None
        if request.content:
            content = [item.model_dump() for item in request.content]
        
        # 调用生成服务
        result = generation_service.generate_game(
            topic=request.topic,
            content=content,
            game_type=request.game_type,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成游戏失败: {str(e)}")

@router.post("/courseware", response_model=GenerateResponse, summary="生成课件")
async def generate_courseware(request: GenerateCoursewareRequest):
    """
    生成课件
    
    - **topic**: 课件主题
    - **type**: 课件类型 (ppt, word, animation, game)
    - **content**: 课件内容（可选）
    - **outline**: 课件大纲（可选）
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 转换请求数据为服务所需格式
        content = None
        if request.content:
            content = [item.model_dump() for item in request.content]
        
        outline = None
        if request.outline:
            outline = request.outline.model_dump()
        
        # 调用生成服务
        result = generation_service.generate_courseware(
            topic=request.topic,
            type=request.type,
            content=content,
            outline=outline,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成课件失败: {str(e)}")

@router.post("/ppt/ai", response_model=GenerateResponse, summary="使用AI生成PPT")
async def generate_ppt_with_ai(request: GeneratePPTWithAIRequest):
    """
    使用AI生成PPT
    
    - **topic**: PPT主题
    - **requirements**: 自定义要求（可选）
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 调用AI生成服务
        result = generation_service.generate_ppt_with_ai(
            topic=request.topic,
            requirements=request.requirements,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成PPT失败: {str(e)}")

@router.post("/ppt/ai/enhance", response_model=GenerateResponse, summary="使用AI增强PPT内容")
async def enhance_ppt_with_ai(request: EnhancePPTWithAIRequest):
    """
    使用AI增强PPT内容
    
    - **topic**: PPT主题
    - **content**: PPT内容
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 转换请求数据为服务所需格式
        content = [item.model_dump() for item in request.content]
        
        # 调用AI增强服务
        result = generation_service.enhance_ppt_with_ai(
            topic=request.topic,
            content=content,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI增强PPT失败: {str(e)}")

@router.post("/lesson-plan/ai", response_model=GenerateResponse, summary="使用AI生成教案")
async def generate_lesson_plan_with_ai(request: GenerateLessonPlanWithAIRequest):
    """
    使用AI生成教案
    
    - **topic**: 教案主题
    - **requirements**: 自定义要求（可选）
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 调用AI生成服务
        result = generation_service.generate_lesson_plan_with_ai(
            topic=request.topic,
            requirements=request.requirements,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成教案失败: {str(e)}")

@router.post("/lesson-plan/ai/from-ppt", response_model=GenerateResponse, summary="从PPT内容生成AI增强教案")
async def generate_lesson_plan_from_ppt_with_ai(request: GenerateLessonPlanFromPPTWithAIRequest):
    """
    从PPT内容生成AI增强教案
    
    - **topic**: 教案主题
    - **ppt_content**: PPT内容
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 转换请求数据为服务所需格式
        ppt_content = [item.model_dump() for item in request.ppt_content]
        
        # 调用AI生成服务
        result = generation_service.generate_lesson_plan_from_ppt_with_ai(
            topic=request.topic,
            ppt_content=ppt_content,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成教案失败: {str(e)}")

@router.post("/game/ai", response_model=GenerateResponse, summary="使用AI生成游戏")
async def generate_game_with_ai(request: GenerateGameWithAIRequest):
    """
    使用AI生成游戏
    
    - **topic**: 游戏主题
    - **game_type**: 游戏类型 (quiz, memory, matching)
    - **requirements**: 自定义要求（可选）
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 调用AI生成服务
        result = generation_service.generate_game_with_ai(
            topic=request.topic,
            game_type=request.game_type,
            requirements=request.requirements,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成游戏失败: {str(e)}")

@router.post("/game/ai/enhance", response_model=GenerateResponse, summary="使用AI增强游戏内容")
async def enhance_game_with_ai(request: EnhanceGameWithAIRequest):
    """
    使用AI增强游戏内容
    
    - **topic**: 游戏主题
    - **content**: 游戏内容
    - **game_type**: 游戏类型
    - **output_filename**: 输出文件名（可选）
    """
    try:
        # 转换请求数据为服务所需格式
        content = [item.model_dump() for item in request.content]
        
        # 调用AI增强服务
        result = generation_service.enhance_game_with_ai(
            topic=request.topic,
            content=content,
            game_type=request.game_type,
            output_filename=request.output_filename
        )
        
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI增强游戏失败: {str(e)}")
