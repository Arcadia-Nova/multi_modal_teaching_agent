from fastapi import APIRouter, Depends, File, UploadFile, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.models import FileType, UploadedFile
from app.services.input_service import InputService
from app.db.session import get_db
from app.services.parse_service import parse_video_file

router = APIRouter()

@router.post("/voice")
async def voice_input(
    session_id: str = Depends(deps.get_session_id),
    audio: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    service = InputService(db)
    text = await service.process_voice(session_id, audio)
    # 将文字交给对话服务处理（通常会在调用此接口后前端再发一条文本消息，或者在这里直接调用对话服务）
    return {"text": text, "session_id": session_id}

@router.post("/text")
async def text_input(
    request: dict,
    session_id: str = Depends(deps.get_session_id),
    db: Session = Depends(get_db)
):
    text = request.get("text")
    service = InputService(db)
    processed_text = service.process_text(session_id, text)
    # 返回后前端应继续与对话服务交互
    return {"text": processed_text, "session_id": session_id}

@router.post("/upload")
async def upload_reference(
    session_id: str = Depends(deps.get_session_id),
    file: UploadFile = File(...),
    reference_note: str = Form(None),
    db: Session = Depends(get_db)
):
    service = InputService(db)
    file_id = await service.upload_reference(session_id, file, reference_note)
    return {"file_id": file_id, "message": "上传成功，正在后台解析"}


@router.post("/upload/video")
async def upload_reference(
        background_tasks: BackgroundTasks,
        session_id: str = Depends(deps.get_session_id),
        file: UploadFile = File(...),
        reference_note: str = Form(None),
        db: Session = Depends(get_db)
):
    service = InputService(db)
    file_id = await service.upload_reference(session_id, file, reference_note)

    # 获取刚保存的文件记录
    file_record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if file_record.file_type == FileType.VIDEO:
        background_tasks.add_task(parse_video_file, file_id, file_record.file_path)

    return {"file_id": file_id, "message": "上传成功，视频正在后台解析"}

@router.put("/upload/{file_id}/note")
async def add_reference_note(
    file_id: str,
    note: str,
    db: Session = Depends(get_db)
):
    service = InputService(db)
    service.add_reference_note(file_id, note)
    return {"message": "参考说明已添加"}