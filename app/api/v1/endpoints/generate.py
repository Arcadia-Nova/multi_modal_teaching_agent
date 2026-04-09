from fastapi import APIRouter, HTTPException
from app.api.v1.models.generate import GeneratePPTRequest, GenerateCoursewareRequest, GenerateResponse
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

@router.post("/courseware", response_model=GenerateResponse, summary="生成课件")
async def generate_courseware(request: GenerateCoursewareRequest):
    """
    生成课件
    
    - **topic**: 课件主题
    - **type**: 课件类型 (ppt, word, animation)
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
