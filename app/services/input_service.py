import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.multimodal.voice_transcriber import VoiceTranscriber
from app.models.reference import UploadedFile, FileType
from app.models.conversation import Message
from app.utils.file_utils import save_upload_file
from app.config import settings


class InputService:
    def __init__(self, db: Session):
        self.db = db
        self.transcriber = VoiceTranscriber()

    async def process_voice(self, session_id: str, audio_file) -> str:
        """处理语音：保存音频 -> 转文字 -> 保存消息 -> 返回文字"""
        # 1. 保存音频文件
        audio_dir = os.path.join(settings.UPLOAD_DIR, session_id, "audio")
        audio_path = await save_upload_file(audio_file, audio_dir)

        # 2. 转文字
        text = await self.transcriber.transcribe(audio_path)

        # 3. 保存消息到数据库
        message = Message(
            session_id=session_id,
            role="user",
            content=text,
            raw_audio_path=audio_path
        )
        self.db.add(message)
        self.db.commit()

        return text

    def process_text(self, session_id: str, text: str) -> str:
        """处理文字输入：保存消息，返回文本"""
        message = Message(
            session_id=session_id,
            role="user",
            content=text
        )
        self.db.add(message)
        self.db.commit()
        return text

    async def upload_reference(self, session_id: str, file, reference_note: str = None) -> str:
        """上传参考资料，保存记录，返回 file_id"""
        import uuid
        file_id = str(uuid.uuid4())
        file_dir = os.path.join(settings.UPLOAD_DIR, session_id, "refs")
        file_path = await save_upload_file(file, file_dir)

        # 判断文件类型
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ['.pdf']:
            file_type = FileType.PDF
        elif ext in ['.docx']:
            file_type = FileType.DOCX
        elif ext in ['.pptx']:
            file_type = FileType.PPTX
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            file_type = FileType.IMAGE
        elif ext in ['.mp4', '.avi', '.mov']:
            file_type = FileType.VIDEO
        else:
            file_type = FileType.OTHER

        uploaded_file = UploadedFile(
            session_id=session_id,
            file_id=file_id,
            original_name=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=os.path.getsize(file_path),
            reference_note=reference_note,
            parsed_status="pending",
            uploaded_at=datetime.now()
        )
        self.db.add(uploaded_file)
        self.db.commit()

        # 触发异步解析（可使用 BackgroundTasks）
        # await trigger_parsing(file_id)

        return file_id

    def add_reference_note(self, file_id: str, note: str):
        """为已有文件添加参考说明"""
        file_record = self.db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
        if file_record:
            file_record.reference_note = note
            self.db.commit()