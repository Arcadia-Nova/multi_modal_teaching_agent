import os

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.api.v1.models.common import FileUploadResponse, NoteUpdateResponse, ParsedResultResponse
from app.services.input_service import InputService

router = APIRouter()


def get_input_service(db: Session = Depends(deps.get_db_session)) -> InputService:
    return InputService(db)


@router.post("/file", response_model=FileUploadResponse)
async def upload_file(
        session_id: str = Depends(deps.get_session_id),
        file: UploadFile = File(...),
        reference_note: Optional[str] = Form(None),
        background_tasks: BackgroundTasks = None,
        input_svc: InputService = Depends(get_input_service)
):
    """上传参考资料，支持PDF/Word/PPT/图片/视频"""
    # 校验文件类型
    allowed_extensions = ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.mp4' , '.mp3']
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=415, detail=f"不支持的文件类型: {ext}")

    # 调用服务层保存并触发异步解析
    file_id = await input_svc.upload_reference(
        session_id=session_id,
        file=file,
        reference_note=reference_note,
        # background_tasks=background_tasks
    )
    return FileUploadResponse(
        file_id=file_id,
        file_name=file.filename,
        message="文件上传成功，后台解析中"
    )


@router.put("/{file_id}/note", response_model=NoteUpdateResponse)
def add_reference_note(
        file_id: str,
        note: str,
        input_svc: InputService = Depends(get_input_service)
):
    """为已上传的文件添加参考说明"""
    success = input_svc.add_reference_note(file_id, note)
    if not success:
        raise HTTPException(status_code=404, detail="文件不存在")
    return NoteUpdateResponse(message="参考说明已更新")


@router.get("/{file_id}/parsed", response_model=ParsedResultResponse)
def get_parsed_result(
        file_id: str,
        input_svc: InputService = Depends(get_input_service)
):
    """获取文件的解析结果（文本/OCR/视频摘要）"""
    result = input_svc.get_parsed_result(file_id)
    if not result:
        raise HTTPException(status_code=404, detail="文件不存在或尚未解析")
    return ParsedResultResponse(
        file_id=file_id,
        parsed_status=result["status"],
        summary=result.get("summary"),
        details=result.get("details")
    )

